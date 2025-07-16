# React CLI Generator - User Guide

## 🚀 Installation

1. **Download the script**
   - Save the Python script in a file named `cli.py`
   - Place it at the root of your React project or in an accessible folder

2. **Make the script executable** (Linux/Mac)
   ```bash
   chmod +x cli.py
   ```

3. **Check Python**
   - Make sure you have Python 3.6+ installed
   ```bash
   python --version
   ```

## 📖 Usage

### General syntax
```bash
python cli.py react g <type> <path/Name>
```

### Arguments

-   `command`: Always `react`.
-   `action`: `generate` or alias `g`.

### Available types
- `c` or `component`: Generates a React component
- `s` or `service`: Generates a service
- `h` or `hook`: Generates a custom hook
- `r` or `redux`: Generates a custom redux slice
- `ctx` or `context`: Generates a custom react context

## 🎯 Smart naming

The CLI automatically handles name formatting according to React conventions:

### Services
```bash
# Input → Output
python cli.py react g s services/auth         → AuthService.ts
python cli.py react g s services/user         → UserService.ts
python cli.py react g s api/payment           → PaymentService.ts
python cli.py react g s authService           → AuthService.ts (avoids duplication)
```

### Components
```bash
# Input → Output
python cli.py react g c components/formModal  → FormModal/
python cli.py react g c ui/button             → Button/
python cli.py react g c userProfile           → UserProfile/
python cli.py react g c user-profile          → UserProfile/ (handles kebab-case)
python cli.py react g c user_profile          → UserProfile/ (handles snake_case)
```

### Hooks
```bash
# Input → Output
python cli.py react g h hooks/fetchData       → useFetchData.ts
python cli.py react g h localStorage          → useLocalStorage.ts
python cli.py react g h useAuth               → useAuth.ts (detects prefix)
python cli.py react g h auth                  → useAuth.ts
```

## 📝 Concrete examples

### 1. Generate a component

```bash
# Simple component at the root of src/
python cli.py react g c Button

# Component in a subfolder
python cli.py react g c components/ui/Modal

# Component with nested path
python cli.py react g c features/auth/LoginForm
```

**Generated files:**
```
src/
└── components/
    └── ui/
        └── Modal/
            ├── Modal.tsx
            ├── Modal.module.scss
            ├── Modal.test.tsx
            └── Modal.types.ts
```

### 2. Generate a service

```bash
# Authentication service
python cli.py react g s services/AuthService

# API service
python cli.py react g s api/UserApiService
```

**Generated files:**
```
src/
└── services/
    ├── AuthService.ts
    └── AuthService.test.ts
```

### 3. Generate a hook

```bash
# Hook for data fetching
python cli.py react g h hooks/FetchData

# Hook for localStorage
python cli.py react g h useLocalStorage
```

**Note:** The "use" prefix is automatically added if omitted

**Generated files:**
```
src/
└── hooks/
    ├── useFetchData.ts
    └── useFetchData.test.ts
```
#### 4\. Generating a Redux Slice

Generates a `user` slice in `src/store/features/`.

```bash
./react-cli.py react g r store/features/user
````

The script will create the following files in `src/store/features/`:

  - `userSlice.ts`
  - `userSlice.test.ts`

*Note: The name will be converted to camelCase and the `Slice` suffix will be added (e.g., `MyData` becomes `myDataSlice`).*

-----
#### 5\. Generating a Context

Generates a `SessionContext` in `src/contexts/`.

```bash
./react-cli.py react g ctx contexts/Session
```

The script will create a `src/contexts/SessionContext` directory with the following files:

  - `SessionContext.tsx`
  - `SessionContext.types.ts`
  - `SessionContext.test.ts`

*Note: The name will be converted to PascalCase and the `Context` suffix will be added (e.g., `session` becomes `SessionContext`).*

## 🎨 --path option

You can override the default path:

```bash
# Place the component in a specific folder
python cli.py react g c Button --path=shared/components

# Result: src/shared/components/Button/

python cli.py react g c homePage  --path=views    
# Result: src/views//HomePage/
```

## ✅ Results display

When generation succeeds, you'll see:

```
✓ Successfully generated component:
  CREATE src/components/ui/Button/Button.tsx
  CREATE src/components/ui/Button/Button.module.scss
  CREATE src/components/ui/Button/Button.test.tsx
  CREATE src/components/ui/Button/Button.types.ts
```

## ⚠️ Error messages

### Existing file
```
✗ Error: File already exists: src/components/Button/Button.tsx
```

### Invalid name
```
✗ Error: Name must be in PascalCase (e.g., MyComponent)
✗ Error: Hook name must start with 'use' (e.g., useFetchData)
```

## 💡 Usage tips

1. **Component organization**
   ```bash
   # By feature
   python cli.py react g c features/todo/TodoList
   python cli.py react g c features/todo/TodoItem
   
   # By type
   python cli.py react g c components/ui/Button
   python cli.py react g c components/forms/Input
   ```

2. **Services by domain**
   ```bash
   python cli.py react g s api/UserApi
   python cli.py react g s storage/LocalStorageService
   python cli.py react g s auth/TokenService
   ```

3. **Reusable hooks**
   ```bash
   python cli.py react g h useDebounce
   python cli.py react g h useWindowSize
   python cli.py react g h usePrevious
   ```

## 🔧 Advanced configuration

### Modifying templates

You can customize templates in the Python script by modifying the `TEMPLATES` section. For example, to add Redux:

```python
'component': {
    'files': [
        {
            'extension': '.tsx',
            'template': '''import React from 'react';
import { useSelector, useDispatch } from 'react-redux';
// ... your custom template
'''
        }
    ]
}
```

### Adding new types

You can extend the script to support other types like:
- `page`: Complete pages
- `util`: Utility functions
- things you think interesting

## 🚨 Troubleshooting

1. **"src directory not found"**
   - The script will automatically create the src folder if it doesn't exist

2. **Permission denied**
   - On Linux/Mac: `chmod +x cli.py`
   - Or use: `python3 cli.py` instead of `./cli.py`

3. **Python not found**
   - Install Python 3.6+ from python.org
   - On some systems, use `python3` instead of `python`

## 🎯 Recommended workflow

1. **Plan your structure** before generating
2. **Use descriptive names** (UserProfile rather than UP)
3. **Group by feature** for large applications
4. **Test immediately** after generation to verify integration

## 📊 Example of complete structure

```
src/
├── components/
│   ├── common/
│   │   ├── Button/
│   │   └── Input/
│   └── layout/
│       ├── Header/
│       └── Footer/
├── features/
│   ├── auth/
│   │   ├── LoginForm/
│   │   └── RegisterForm/
│   └── dashboard/
│       └── DashboardWidget/
├── hooks/
│   ├── useAuth.ts
│   └── useFetch.ts
└── services/
    ├── api/
    │   └── ApiService.ts
    └── storage/
        └── StorageService.ts
```

This structure can be generated entirely with the CLI!


# MIT License

Copyright (c) 2025 Christ Bouka

Permission is hereby granted, free of charge, to any person obtaining a copy  
of this software and associated documentation files (the “Software”), to deal  
in the Software without restriction, including without limitation the rights  
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell  
copies of the Software, and to permit persons to whom the Software is  
furnished to do so, subject to the following conditions:

> **The above copyright notice and this permission notice shall be included in  
> all copies or substantial portions of the Software.**

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR  
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,  
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE  
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER  
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,  
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN  
THE SOFTWARE.
