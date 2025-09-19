# AI Code Assistant Guidelines for CONVAI

## Project Context

CONVAI is a conversational AI project that welcomes AI-assisted development. This document provides specific guidelines for AI code assistants working with this codebase.

## Code Generation Guidelines

### 1. Style and Conventions
- Follow consistent naming conventions
- Use clear, descriptive variable and function names
- Include appropriate comments for complex logic
- Maintain consistent indentation and formatting

### 2. Architecture Patterns
- Prefer modular, reusable components
- Follow separation of concerns principles
- Use appropriate design patterns for the use case
- Consider scalability and maintainability

### 3. Error Handling
- Implement comprehensive error handling
- Use appropriate exception types
- Provide meaningful error messages
- Include fallback mechanisms where appropriate

### 4. Testing Requirements
- Generate unit tests for new functions
- Include integration tests for complex features
- Ensure good test coverage
- Use descriptive test names and assertions

### 5. Documentation Standards
- Document public APIs and interfaces
- Include usage examples in documentation
- Update README files when adding new features
- Maintain inline comments for complex algorithms

## AI-Specific Considerations

### Code Review
- AI-generated code should be reviewed for correctness
- Validate that generated code follows project patterns
- Ensure security best practices are followed
- Check for potential performance issues

### Incremental Development
- Make small, focused changes
- Test each change thoroughly
- Commit changes with descriptive messages
- Document the rationale for AI-assisted decisions

### Collaboration
- Indicate when AI assistance was used
- Provide context for AI-generated solutions
- Be prepared to explain AI-suggested approaches
- Consider alternative solutions when appropriate

## Prohibited Practices

- Do not generate code that violates the MIT license
- Avoid creating security vulnerabilities
- Do not introduce unnecessary complexity
- Avoid breaking existing functionality
- Do not generate malicious or harmful code

## Quality Assurance

AI assistants should ensure:
- Code compiles without errors
- Tests pass successfully
- No security vulnerabilities are introduced
- Performance is not significantly degraded
- Code follows established patterns

## Getting Help

If AI assistants encounter unclear requirements or need clarification:
- Review existing code patterns
- Check documentation and comments
- Consider opening an issue for discussion
- Follow established project conventions as fallback