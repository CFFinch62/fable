# Contributing to FABLE

Thank you for your interest in contributing to FABLE (Forth Animated Beginners Learning Environment)! We welcome contributions from the community.

## How to Contribute

### Reporting Bugs

If you find a bug, please open an issue with:
- A clear, descriptive title
- Steps to reproduce the problem
- Expected behavior vs. actual behavior
- Your environment (OS, Python version, PyQt6 version)
- Screenshots if applicable

### Suggesting Features

We love new ideas! Please open an issue with:
- A clear description of the feature
- Why it would be useful for learning Forth
- Any implementation ideas you have

### Contributing Code

1. **Fork the repository**
   ```bash
   gh repo fork CFFinch62/fable --clone
   cd fable
   ```

2. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow the existing code style
   - Add comments for complex logic
   - Update documentation if needed

4. **Test your changes**
   ```bash
   python3 fable.py
   # Test the feature manually
   ```

5. **Commit your changes**
   ```bash
   git add .
   git commit -m "Add feature: description"
   ```

6. **Push and create a pull request**
   ```bash
   git push origin feature/your-feature-name
   gh pr create
   ```

## Development Guidelines

### Code Style

- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add docstrings to classes and functions
- Keep functions focused and small

### Project Structure

- `fable/` - Main application code
  - `interpreter/` - Forth interpreter implementation
  - `widgets/` - UI components
  - `utils/` - Utility functions
- `libraries/` - Bundled Forth libraries
- `examples/` - Example Forth programs
- `docs/` - Documentation
- `tests/` - Test files

### Adding New Forth Words

To add a new primitive word:

1. Add the implementation in `fable/interpreter/primitives.py`
2. Register it in the `create_primitives()` function
3. Add documentation with stack effect notation
4. Add examples in the docstring
5. Update `docs/LANGUAGE_REFERENCE.md`

### Adding Examples

Example programs should:
- Focus on one concept
- Include comments explaining what's happening
- Use clear, descriptive names
- Be suitable for beginners

### Adding Libraries

Library files should:
- Be well-documented with comments
- Follow Forth naming conventions
- Include usage examples
- Be added to `libraries/README.md`

## Testing

Currently, FABLE uses manual testing. When adding features:
- Test in both REPL and Editor modes
- Test with step-through debugging (F10)
- Verify stack animations work correctly
- Test with both dark and light themes

## Documentation

When adding features, update:
- `README.md` - If it's a major feature
- `docs/USERGUIDE.md` - For user-facing features
- `docs/LANGUAGE_REFERENCE.md` - For new Forth words
- Code comments and docstrings

## Questions?

Feel free to open an issue with the "question" label if you need help or clarification.

## Code of Conduct

Be respectful, constructive, and welcoming to all contributors. We're here to learn and build together!

---

Thank you for contributing to FABLE! 🎉

