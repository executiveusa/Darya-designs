# Skill: Generate Production Code

## Purpose
Generate production-ready code that follows industry best practices, design patterns, and maintains consistency with existing codebases.

## When to Use
- Creating new features or modules
- Adding new API endpoints
- Implementing business logic
- Setting up new services or microservices
- Bootstrapping new projects

## Prerequisites
- Clear requirements or user story
- Target codebase accessible
- Identified technology stack
- Understanding of existing patterns

## Execution Steps

### 1. Analyze Context
```
Read:
- Existing code in similar modules
- Architecture patterns used
- Naming conventions
- Error handling patterns
- Testing patterns
```

### 2. Generate Code
```
Create:
- Function/class signatures with types
- Implementation with comments
- Error handling
- Input validation
- Logging statements
```

### 3. Ensure Quality
```
Verify:
- TypeScript/Python types are correct
- Follows linting rules
- Includes JSDoc/docstrings
- Error cases handled
- No security vulnerabilities
```

### 4. Create Tests
```
Generate:
- Unit tests for main logic
- Edge case tests
- Error condition tests
- Integration test stubs
```

### 5. Documentation
```
Add:
- Code comments explaining complex logic
- README section for new module
- Example usage
- Configuration requirements
```

## Output Format
```
Generated Files:
  - Implementation file(s)
  - Test file(s)
  - Documentation updates

Quality Metrics:
  - Lines of code
  - Cyclomatic complexity
  - Test coverage percentage
  - Linting score
```

## Parameters
- **Language**: typescript | python | go | rust | java
- **Style**: functional | object-oriented | mixed
- **Testing**: unit | integration | e2e
- **Documentation Level**: minimal | standard | comprehensive

## Success Criteria
- [ ] Code passes linter
- [ ] All tests pass
- [ ] >80% test coverage
- [ ] TypeScript: No type errors
- [ ] Python: Type hints present
- [ ] Documentation complete
- [ ] No security issues

## Common Issues & Solutions

### Issue: Generated code doesn't match existing style
**Solution**: Run through Prettier/Black, then manual review

### Issue: Type errors in TypeScript
**Solution**: Re-read tsconfig and existing patterns, regenerate with correct types

### Issue: Missing error handling
**Solution**: Review error patterns in similar modules, add try-catch blocks

## Integration Points
- VSCode extension for quick generation
- Pre-commit hooks to validate
- CI/CD pipeline for testing generated code
- Code review workflow integration

## Related Skills
- `code-generation/architecture-design` - For overall design
- `testing/test-case-generator` - For comprehensive tests
- `code-review/quality-gates` - For validation
