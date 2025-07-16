#!/usr/bin/env python3
"""
React CLI Generator - A Python script to generate React components, services, and hooks
Similar to Angular CLI functionality
"""

import os
import sys
import re
import argparse
from pathlib import Path
from typing import Dict, List, Tuple


# ANSI color codes for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


# Template configurations
TEMPLATES = {
    'component': {
        'files': [
            {
                'extension': '.tsx',
                'template': '''import React from 'react';
import styles from './{name}.module.scss';
import {{ {name}Props }} from './{name}.types';

const {name}: React.FC<{name}Props> = ({{ }}) => {{
  return (
    <div className={{styles.container}}>
      <h1>{name} Component</h1>
    </div>
  );
}};

export default {name};
'''
            },
            {
                'extension': '.module.scss',
                'template': '''.container {{
  // Add your styles here
}}
'''
            },
            {
                'extension': '.test.tsx',
                'template': '''import React from 'react';
import {{ render, screen }} from '@testing-library/react';
import {name} from './{name}';

describe('{name}', () => {{
  it('renders without crashing', () => {{
    render(<{name} />);
    const element = screen.getByText('{name} Component');
    expect(element).toBeInTheDocument();
  }});
}});
'''
            },
            {
                'extension': '.types.ts',
                'template': '''export interface {name}Props {{
  // Define your props here
}}
'''
            }
        ]
    },
    'service': {
        'files': [
            {
                'extension': '.ts',
                'template': '''export class {name} {{
  private static instance: {name};

  private constructor() {{
    // Private constructor for singleton pattern
  }}

  public static getInstance(): {name} {{
    if (!{name}.instance) {{
      {name}.instance = new {name}();
    }}
    return {name}.instance;
  }}

  // Add your service methods here
  public async getData(): Promise<any> {{
    // Implement your logic
    return {{}};
  }}
}}

export default {name}.getInstance();
'''
            },
            {
                'extension': '.test.ts',
                'template': '''import {{ {name} }} from './{name}';

describe('{name}', () => {{
  it('should be a singleton', () => {{
    const instance1 = {name}.getInstance();
    const instance2 = {name}.getInstance();
    expect(instance1).toBe(instance2);
  }});

  it('should have getData method', () => {{
    const instance = {name}.getInstance();
    expect(instance.getData).toBeDefined();
  }});
}});
'''
            }
        ]
    },
    'hook': {
        'files': [
            {
                'extension': '.ts',
                'template': '''import {{ useState, useEffect }} from 'react';

export const {name} = () => {{
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {{
    // Add your hook logic here
  }}, []);

  return {{ data, loading, error }};
}};

export default {name};
'''
            },
            {
                'extension': '.test.ts',
                'template': '''import {{ renderHook }} from '@testing-library/react-hooks';
import {{ {name} }} from './{name}';

describe('{name}', () => {{
  it('should return initial state', () => {{
    const {{ result }} = renderHook(() => {name}());

    expect(result.current.data).toBeNull();
    expect(result.current.loading).toBe(false);
    expect(result.current.error).toBeNull();
  }});
}});
'''
            }
        ]
    }
}


class ReactCLIGenerator:
    def __init__(self):
        self.src_path = Path('src')

    def validate_name(self, name: str, type: str) -> bool:
        """Validate naming conventions"""
        if type == 'hook':
            # Hooks must start with 'use'
            return name.startswith('use') and name[3].isupper() if len(name) > 3 else False
        else:
            # Components and services must be PascalCase
            return bool(re.match(r'^[A-Z][a-zA-Z0-9]*$', name))

    def format_name(self, name: str, type: str) -> str:
        """Format name according to conventions"""
        # First, ensure PascalCase for the base name
        base_name = self.to_pascal_case(name)

        if type == 'hook':
            # Ensure hook starts with 'use'
            if not base_name.startswith('use'):
                base_name = 'use' + base_name
            return base_name
        elif type == 'service':
            # Add 'Service' suffix if not already present
            if not base_name.endswith('Service'):
                base_name = base_name + 'Service'
            return base_name
        else:
            # For components, just ensure PascalCase
            return base_name

    def to_pascal_case(self, name: str) -> str:
        """Convert any string to PascalCase"""
        # Handle different naming conventions
        # Remove Service suffix if it exists (we'll add it back properly)
        name = re.sub(r'[Ss]ervice$', '', name)

        # Handle camelCase, kebab-case, snake_case
        # Split by common delimiters
        parts = re.split(r'[-_\s]+', name)

        # Also split camelCase
        final_parts = []
        for part in parts:
            # Split camelCase words
            camel_parts = re.findall(r'[A-Z][a-z]*|[a-z]+', part)
            if camel_parts:
                final_parts.extend(camel_parts)
            elif part:  # If no camelCase pattern found, use the part as is
                final_parts.append(part)

        # Capitalize each part and join
        return ''.join(word.capitalize() for word in final_parts if word)

    def create_file(self, file_path: Path, content: str) -> bool:
        """Create a file with content"""
        try:
            # Check if file already exists
            if file_path.exists():
                print(f"{Colors.RED}✗ Error: File already exists: {file_path}{Colors.RESET}")
                return False

            # Create directories if they don't exist
            file_path.parent.mkdir(parents=True, exist_ok=True)

            # Write file
            file_path.write_text(content)
            return True
        except Exception as e:
            print(f"{Colors.RED}✗ Error creating file {file_path}: {str(e)}{Colors.RESET}")
            return False

    def generate(self, type: str, path: str, name: str) -> bool:
        """Generate files based on type"""
        # Format and validate name
        original_name = name
        formatted_name = self.format_name(name, type)

        # Show the formatted name if it's different from input
        if original_name.lower() != formatted_name.lower():
            print(f"{Colors.BLUE}ℹ Using formatted name: {formatted_name}{Colors.RESET}")

        if not self.validate_name(formatted_name, type):
            if type == 'hook':
                print(f"{Colors.RED}✗ Error: Hook name must start with 'use' (e.g., useFetchData){Colors.RESET}")
            else:
                print(f"{Colors.RED}✗ Error: Name must be in PascalCase (e.g., MyComponent){Colors.RESET}")
            return False

        # Get template configuration
        if type not in TEMPLATES:
            print(f"{Colors.RED}✗ Error: Unknown type '{type}'{Colors.RESET}")
            return False

        template_config = TEMPLATES[type]

        # Construct base path
        base_path = self.src_path / path if path else self.src_path

        # For components, create a folder with the component name
        if type == 'component':
            base_path = base_path / formatted_name

        # Create all files
        created_files = []
        all_success = True

        for file_config in template_config['files']:
            file_name = formatted_name + file_config['extension']
            file_path = base_path / file_name

            # Replace placeholders in template
            content = file_config['template'].format(name=formatted_name)

            if self.create_file(file_path, content):
                created_files.append(file_path)
            else:
                all_success = False

        # Display results
        if all_success and created_files:
            print(f"\n{Colors.GREEN}✓ Successfully generated {type}:{Colors.RESET}")
            for file_path in created_files:
                try:
                    # Try to get relative path from current directory
                    relative_path = file_path.relative_to(Path.cwd())
                except ValueError:
                    # If that fails, just use the absolute path
                    relative_path = file_path
                print(f"  {Colors.GREEN}CREATE{Colors.RESET} {str(relative_path).replace(os.sep, '/')}")
            print()

        return all_success


def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='React CLI Generator')

    # Main command
    parser.add_argument('command', choices=['react'], help='Main command')

    # Subcommand
    parser.add_argument('action', choices=['g', 'generate'], help='Action to perform')

    # Type
    parser.add_argument('type', choices=['c', 'component', 's', 'service', 'h', 'hook'],
                        help='Type to generate (c=component, s=service, h=hook)')

    # Path/Name
    parser.add_argument('path_name', help='Path and name (e.g., components/ui/Button)')

    # Optional path override
    parser.add_argument('--path', help='Override default path')

    return parser.parse_args()


def main():
    """Main entry point"""
    try:
        args = parse_arguments()

        # Normalize type
        type_map = {
            'c': 'component',
            's': 'service',
            'h': 'hook'
        }
        generate_type = type_map.get(args.type, args.type)

        # Parse path and name
        path_parts = args.path_name.split('/')
        name = path_parts[-1]
        path = '/'.join(path_parts[:-1]) if len(path_parts) > 1 else ''

        # Override path if --path is provided
        if args.path:
            path = args.path

        # Create generator and generate files
        generator = ReactCLIGenerator()

        # Check if src directory exists
        if not generator.src_path.exists():
            print(f"{Colors.YELLOW}⚠ Warning: 'src' directory not found. Creating it...{Colors.RESET}")
            generator.src_path.mkdir(exist_ok=True)

        success = generator.generate(generate_type, path, name)

        sys.exit(0 if success else 1)

    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Operation cancelled by user{Colors.RESET}")
        sys.exit(1)
    except Exception as e:
        print(f"{Colors.RED}✗ Unexpected error: {str(e)}{Colors.RESET}")
        sys.exit(1)


if __name__ == '__main__':
    main()