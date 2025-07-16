#!/usr/bin/env python3
"""
# SPDX-License-Identifier: MIT
# © 2025 Christ Bouka <christbouka14@yahoo.fr>
#
# Signed-off-by: Christ Bouka <christbouka14@yahoo.fr>

React CLI Generator - A Python script to generate React components, services, hooks, redux slices, and contexts.
Similar to Angular CLI functionality.
"""

import os
import sys
import re
import argparse
from pathlib import Path
from typing import Dict, Tuple


# ANSI color codes for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


# Template configurations
TEMPLATES: Dict[str, Dict] = {
    'component': {
        'files': [
            {
                'extension': '.tsx',
                'template': '''import React from 'react';
import styles from './{name}.module.scss';
import {{ {name}Props }} from './{name}.types';

const {name}: React.FC<{name}Props> = ({{}}) => {{
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
                'template': '''import singleton from './{name}';

describe('{name}', () => {{
  it('should be a singleton', () => {{
    const instance1 = singleton;
    const instance2 = singleton;
    expect(instance1).toBe(instance2);
  }});

  it('should have getData method', () => {{
    const instance = singleton;
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
    },
    'redux': {
        'files': [
            {
                'extension': '.ts',
                'template': '''import {{ createSlice, PayloadAction }} from '@reduxjs/toolkit';
// import type {{ RootState }} from '../store'; // Adjust path to your root state

// Define a type for the slice state
export interface {pascalName}State {{
  value: number;
  status: 'idle' | 'loading' | 'failed';
}}

// Define the initial state using that type
const initialState: {pascalName}State = {{
  value: 0,
  status: 'idle',
}};

export const {name} = createSlice({{
  name: '{camelName}',
  initialState,
  // The `reducers` field lets us define reducers and generate associated actions
  reducers: {{
    increment: (state) => {{
      state.value += 1;
    }},
    decrement: (state) => {{
      state.value -= 1;
    }},
    // Use the PayloadAction type to declare the contents of `action.payload`
    incrementByAmount: (state, action: PayloadAction<number>) => {{
      state.value += action.payload;
    }},
  }},
}});

export const {{ increment, decrement, incrementByAmount }} = {name}.actions;

// The function below is called a selector and allows us to select a value from
// the state. Selectors can also be defined inline where they're used instead of
// in the slice file. For example: `useSelector((state: RootState) => state.{camelName}.value)`
// export const selectCount = (state: RootState) => state.{camelName}.value;

export default {name}.reducer;
'''
            },
            {
                'extension': '.test.ts',
                'template': '''import reducer, {{ {pascalName}State, increment, decrement }} from './{name}';

describe('{name} reducer', () => {{
  const initialState: {pascalName}State = {{
    value: 3,
    status: 'idle',
  }};

  it('should handle initial state', () => {{
    expect(reducer(undefined, {{ type: 'unknown' }})).toEqual({{
        value: 0,
        status: 'idle',
    }});
  }});

  it('should handle increment', () => {{
    const actual = reducer(initialState, increment());
    expect(actual.value).toEqual(4);
  }});

  it('should handle decrement', () => {{
    const actual = reducer(initialState, decrement());
    expect(actual.value).toEqual(2);
  }});
}});
'''
            }
        ]
    },
    'context': {
        'files': [
            {
                'extension': '.tsx',
                'template': '''import React, {{ createContext, useContext, useState, useMemo }} from 'react';
import {{ {name}Props, {name}Type }} from './{name}.types';

const {name}Context = createContext<{name}Type | undefined>(undefined);

export const {name}Provider: React.FC<{name}Props> = ({{ children }}) => {{
  const [value, setValue] = useState<string>('Default Value'); // Example state

  const contextValue = useMemo(() => ({{
    value,
    setValue,
  }}), [value]);

  return (
    <{name}Context.Provider value={{contextValue}}>
      {{children}}
    </{name}Context.Provider>
  );
}};

export const use{pascalName} = (): {name}Type => {{
  const context = useContext({name}Context);
  if (context === undefined) {{
    throw new Error(`use{pascalName} must be used within a {name}Provider`);
  }}
  return context;
}};
'''
            },
            {
                'extension': '.types.ts',
                'template': '''import React from 'react';

export interface {name}Props {{
  children: React.ReactNode;
}}

export interface {name}Type {{
  value: string;
  setValue: React.Dispatch<React.SetStateAction<string>>;
}}
'''
            },
            {
                'extension': '.test.tsx',
                'template': '''import React from 'react';
import {{ render, screen, act }} from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import {{ {name}Provider, use{pascalName} }} from './{name}';

const TestComponent: React.FC = () => {{
  const {{ value, setValue }} = use{pascalName}();
  return (
    <div>
      <span>{{value}}</span>
      <button onClick={{() => setValue('New Value')}}>Change</button>
    </div>
  );
}};

describe('{name}', () => {{
  it('provides the default value and allows updates', async () => {{
    render(
      <{name}Provider>
        <TestComponent />
      </{name}Provider>
    );

    // Check initial value
    expect(screen.getByText('Default Value')).toBeInTheDocument();

    // Update value
    const button = screen.getByRole('button', {{ name: /change/i }});
    await userEvent.click(button);

    // Check updated value
    expect(screen.getByText('New Value')).toBeInTheDocument();
  }});

  it('throws an error when used outside of a provider', () => {{
    // Suppress console.error for this expected error
    jest.spyOn(console, 'error').mockImplementation(() => {{}});

    expect(() => render(<TestComponent />)).toThrow('use{pascalName} must be used within a {name}Provider');

    jest.restoreAllMocks();
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

    def to_pascal_case(self, name: str) -> str:
        """Convert any string to PascalCase."""
        parts = re.split(r'[A-Z]?[a-z]+|[A-Z]+(?![a-z])', name)
        if len(parts) > 1:  # Likely camelCase or mixedCase
            name = ' '.join(re.findall(r'[A-Z]?[a-z]+|[A-Z]+(?![a-z])', name))

        return "".join(word.capitalize() for word in re.split(r'[-_\s]+', name))

    def to_camel_case(self, name: str) -> str:
        """Convert string to camelCase."""
        pascal = self.to_pascal_case(name)
        if not pascal:
            return ''
        return pascal[0].lower() + pascal[1:]

    def format_name(self, name: str, type: str) -> Tuple[str, str, str]:
        """Formats name and returns a tuple of (formatted_name, pascal_case_base, camel_case_base)."""
        base_name = name

        # Strip common suffixes/prefixes if user included them, to avoid duplication
        if type == 'service' and base_name.lower().endswith('service'):
            base_name = base_name[:-7]
        if type == 'hook' and base_name.lower().startswith('use'):
            base_name = base_name[3:]
        if type == 'redux' and base_name.lower().endswith('slice'):
            base_name = base_name[:-5]
        if type == 'context' and base_name.lower().endswith('context'):
            base_name = base_name[:-7]

        pascal_case = self.to_pascal_case(base_name)
        camel_case = self.to_camel_case(base_name)

        if type == 'hook':
            formatted_name = 'use' + pascal_case
        elif type == 'service':
            formatted_name = pascal_case + 'Service'
        elif type == 'redux':
            formatted_name = camel_case + 'Slice'
        elif type == 'context':
            formatted_name = pascal_case + 'Context'
        else:  # component
            formatted_name = pascal_case

        return formatted_name, pascal_case, camel_case

    def validate_name(self, name: str, type: str) -> bool:
        """Validate naming conventions for the final formatted name."""
        if not name: return False
        if type == 'hook':
            return name.startswith('use') and len(name) > 3 and name[3].isupper()
        if type == 'redux':
            return bool(re.match(r'^[a-z][a-zA-Z0-9]*Slice$', name))
        # Components, services, context must be PascalCase (with appropriate suffixes)
        return bool(re.match(r'^[A-Z][a-zA-Z0-9]*$', name.replace('Service', '').replace('Context', '')))

    def create_file(self, file_path: Path, content: str) -> bool:
        """Create a file with content."""
        try:
            if file_path.exists():
                print(f"{Colors.RED}✗ Error: File already exists: {file_path}{Colors.RESET}")
                return False
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(content)
            return True
        except Exception as e:
            print(f"{Colors.RED}✗ Error creating file {file_path}: {str(e)}{Colors.RESET}")
            return False

    def generate(self, type: str, path: str, name: str) -> bool:
        """Generate files based on type."""
        original_name = name
        formatted_name, pascal_name, camel_name = self.format_name(original_name, type)

        # Show the formatted name if it's different from input
        if original_name.lower() != formatted_name.lower().replace('slice', '').replace('service', '').replace(
                'context', '').replace('use', ''):
            print(f"{Colors.BLUE}ℹ Using formatted name: {Colors.BOLD}{formatted_name}{Colors.RESET}")

        if not self.validate_name(formatted_name, type):
            error_map = {
                'hook': "Hook name must start with 'use' (e.g., useCounter)",
                'redux': "Redux slice name must be camelCase (e.g., myCounter)",
                'component': "Component name must be PascalCase (e.g., MyComponent)",
                'service': "Service name must be PascalCase (e.g., DataService)",
                'context': "Context name must be PascalCase (e.g., UserContext)",
            }
            print(
                f"{Colors.RED}✗ Error: Invalid name. {error_map.get(type, 'Name must be in PascalCase.')}{Colors.RESET}")
            return False

        template_config = TEMPLATES[type]
        base_path = self.src_path / path if path else self.src_path

        # For components and contexts, create a folder with the generated name
        if type in ['component', 'context']:
            base_path = base_path / formatted_name

        created_files = []
        all_success = True

        for file_config in template_config['files']:
            # For redux, the filename *is* the formatted name
            file_name = formatted_name + file_config['extension']
            file_path = base_path / file_name

            content = file_config['template'].format(
                name=formatted_name,
                pascalName=pascal_name,
                camelName=camel_name
            )

            if self.create_file(file_path, content):
                created_files.append(file_path)
            else:
                all_success = False

        if all_success and created_files:
            print(f"\n{Colors.GREEN}✓ Successfully generated {type}:{Colors.RESET}")
            for file_path in created_files:
                try:
                    relative_path = file_path.relative_to(Path.cwd())
                except ValueError:
                    relative_path = file_path
                print(f"  {Colors.GREEN}CREATE{Colors.RESET} {str(relative_path).replace(os.sep, '/')}")
            print()

        return all_success


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='React CLI Generator')
    parser.add_argument('command', choices=['react'], help="The main command, must be 'react'.")
    parser.add_argument('action', choices=['g', 'generate'], help='The action to perform (generate).')
    parser.add_argument(
        'type',
        choices=['c', 'component', 's', 'service', 'h', 'hook', 'r', 'redux', 'ctx', 'context'],
        help='Type to generate (c=component, s=service, h=hook, r=redux, ctx=context).'
    )
    parser.add_argument('path_name', help='Path and name of the schematic (e.g., components/ui/Button).')
    parser.add_argument('--path', help='Override the path determined from path_name.')
    return parser.parse_args()


def main():
    """Main entry point."""
    try:
        args = parse_arguments()

        type_map = {
            'c': 'component',
            's': 'service',
            'h': 'hook',
            'r': 'redux',
            'ctx': 'context'
        }
        generate_type = type_map.get(args.type, args.type)

        path_parts = args.path_name.split('/')
        name = path_parts[-1]
        path = '/'.join(path_parts[:-1]) if len(path_parts) > 1 else ''

        if args.path:
            path = args.path

        generator = ReactCLIGenerator()

        if not generator.src_path.exists():
            print(f"{Colors.YELLOW}⚠ Warning: 'src' directory not found. Creating it...{Colors.RESET}")
            generator.src_path.mkdir(exist_ok=True)

        success = generator.generate(generate_type, path, name)
        sys.exit(0 if success else 1)

    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Operation cancelled by user.{Colors.RESET}")
        sys.exit(1)
    except Exception as e:
        print(f"{Colors.RED}✗ Unexpected error: {str(e)}{Colors.RESET}")
        sys.exit(1)


if __name__ == '__main__':
    main()