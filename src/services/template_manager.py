import json
import os
import glob
from typing import Dict, List, Optional, Tuple
from pathlib import Path

class TemplateManager:
    """Manages server templates and auto-detection of project types"""
    
    def __init__(self, config_dir: str = None):
        if config_dir is None:
            config_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'config')
        
        self.config_dir = config_dir
        self.templates_file = os.path.join(config_dir, 'server_templates.json')
        self.templates = self._load_templates()
    
    def _load_templates(self) -> Dict:
        """Load server templates from JSON file"""
        try:
            with open(self.templates_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {"templates": {}, "categories": {}}
        except json.JSONDecodeError as e:
            print(f"Error loading templates: {e}")
            return {"templates": {}, "categories": {}}
    
    def get_all_templates(self) -> Dict:
        """Get all available templates"""
        return self.templates.get('templates', {})
    
    def get_template(self, template_id: str) -> Optional[Dict]:
        """Get specific template by ID"""
        return self.templates.get('templates', {}).get(template_id)
    
    def get_categories(self) -> Dict:
        """Get all template categories"""
        return self.templates.get('categories', {})
    
    def get_templates_by_category(self, category: str) -> Dict:
        """Get all templates in a specific category"""
        templates = self.get_all_templates()
        return {k: v for k, v in templates.items() if v.get('category') == category}
    
    def detect_project_type(self, project_path: str) -> List[Tuple[str, Dict, float]]:
        """Auto-detect project type based on file markers
        
        Returns:
            List of tuples: (template_id, template_config, confidence_score)
            Sorted by confidence score (highest first)
        """
        if not os.path.exists(project_path):
            return []
        
        detected = []
        templates = self.get_all_templates()
        
        for template_id, template_config in templates.items():
            confidence = self._calculate_confidence(project_path, template_config)
            if confidence > 0:
                detected.append((template_id, template_config, confidence))
        
        # Sort by confidence score (highest first)
        detected.sort(key=lambda x: x[2], reverse=True)
        return detected
    
    def _calculate_confidence(self, project_path: str, template_config: Dict) -> float:
        """Calculate confidence score for a template match"""
        file_markers = template_config.get('file_markers', [])
        required_files = template_config.get('required_files', [])
        
        if not file_markers and not required_files:
            return 0.0
        
        total_markers = len(file_markers) + len(required_files)
        found_markers = 0
        required_found = 0
        
        # Check file markers
        for marker in file_markers:
            if self._file_exists(project_path, marker):
                found_markers += 1
        
        # Check required files (higher weight)
        for required_file in required_files:
            if self._file_exists(project_path, required_file):
                required_found += 1
                found_markers += 2  # Double weight for required files
        
        # Must have all required files
        if required_files and required_found < len(required_files):
            return 0.0
        
        # Calculate confidence score
        max_score = len(file_markers) + (len(required_files) * 2)
        if max_score == 0:
            return 0.0
        
        confidence = found_markers / max_score
        
        # Bonus for having all markers
        if found_markers == max_score:
            confidence += 0.1
        
        return min(confidence, 1.0)
    
    def _file_exists(self, project_path: str, pattern: str) -> bool:
        """Check if file exists, supports glob patterns"""
        if '*' in pattern:
            # Glob pattern
            matches = glob.glob(os.path.join(project_path, pattern))
            return len(matches) > 0
        else:
            # Exact file
            return os.path.exists(os.path.join(project_path, pattern))
    
    def get_suggested_config(self, project_path: str, template_id: str = None) -> Dict:
        """Get suggested server configuration for a project
        
        Args:
            project_path: Path to the project directory
            template_id: Specific template to use, or None for auto-detection
        
        Returns:
            Dictionary with suggested configuration
        """
        if template_id:
            template = self.get_template(template_id)
            if not template:
                return self._get_default_config(project_path)
        else:
            # Auto-detect
            detected = self.detect_project_type(project_path)
            if not detected:
                return self._get_default_config(project_path)
            
            template_id, template, confidence = detected[0]
        
        # Build suggested configuration
        project_name = os.path.basename(project_path)
        
        config = {
            'name': project_name,
            'path': project_path,
            'command': template.get('default_command', ''),
            'port': template.get('default_port'),
            'template_id': template_id,
            'template_name': template.get('name', template_id),
            'category': template.get('category', 'custom')
        }
        
        # Add environment variables if specified
        if 'env_vars' in template:
            config['env_vars'] = template['env_vars']
        
        # Add alternative commands
        if 'alternative_commands' in template:
            config['alternative_commands'] = template['alternative_commands']
        
        return config
    
    def _get_default_config(self, project_path: str) -> Dict:
        """Get default configuration for unknown project types"""
        project_name = os.path.basename(project_path)
        return {
            'name': project_name,
            'path': project_path,
            'command': '',
            'port': None,
            'template_id': 'custom',
            'template_name': 'Custom Server',
            'category': 'custom'
        }
    
    def build_command(self, template_id: str, base_command: str, port: int = None, host: str = None) -> str:
        """Build complete command with port and host parameters
        
        Args:
            template_id: Template identifier
            base_command: Base command to run
            port: Port number (optional)
            host: Host address (optional)
        
        Returns:
            Complete command string
        """
        template = self.get_template(template_id)
        if not template:
            return base_command
        
        command = base_command
        
        # Add port parameter
        if port:
            if template.get('port_inline'):
                # Port goes inline (e.g., "python manage.py runserver 127.0.0.1:8000")
                if host:
                    command += f" {host}:{port}"
                else:
                    command += f" {port}"
            elif template.get('port_flag'):
                # Port uses flag (e.g., "--port 8000")
                port_flag = template['port_flag']
                if not f"{port_flag}" in command:
                    command += f" {port_flag} {port}"
            elif template.get('port_env'):
                # Port uses environment variable - handled separately
                pass
        
        # Add host parameter
        if host and template.get('host_flag'):
            host_flag = template['host_flag']
            if not f"{host_flag}" in command:
                command += f" {host_flag} {host}"
        
        return command.strip()
    
    def get_environment_vars(self, template_id: str, port: int = None, host: str = None) -> Dict[str, str]:
        """Get environment variables for a template
        
        Args:
            template_id: Template identifier
            port: Port number (optional)
            host: Host address (optional)
        
        Returns:
            Dictionary of environment variables
        """
        template = self.get_template(template_id)
        if not template:
            return {}
        
        env_vars = template.get('env_vars', {}).copy()
        
        # Add port environment variable
        if port and template.get('port_env'):
            port_env = template['port_env']
            if port_env == 'ASPNETCORE_URLS':
                # Special case for .NET Core
                protocol = 'https' if port == 443 else 'http'
                host = host or '127.0.0.1'
                env_vars[port_env] = f"{protocol}://{host}:{port}"
            else:
                env_vars[port_env] = str(port)
        
        return env_vars
    
    def validate_project_path(self, project_path: str, template_id: str) -> Tuple[bool, str]:
        """Validate if project path is suitable for the given template
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not os.path.exists(project_path):
            return False, "Project path does not exist"
        
        if not os.path.isdir(project_path):
            return False, "Project path is not a directory"
        
        template = self.get_template(template_id)
        if not template:
            return True, ""  # Custom template, no validation needed
        
        # Check required files
        required_files = template.get('required_files', [])
        for required_file in required_files:
            if not self._file_exists(project_path, required_file):
                return False, f"Required file not found: {required_file}"
        
        return True, ""