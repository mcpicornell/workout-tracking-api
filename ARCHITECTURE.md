# Architecture Guidelines

## Layers (Clean Architecture)
1. **Domain**: Pure business logic and entities. No external dependencies.
2. **Adapters**: Transforms and mediates between domain and infrastructure. Contains logic to map objects between layers.
3. **Infra**: Technical implementation (DB, repositories, settings).

## Dependency Rules
1. **Unidirectional Flow**:
   - `Infra` can call other `Infra` modules, but NEVER `Adapters` or `Domain`.
   - `Adapters` must NOT call other `Adapters`. They facilitate communication between `Infra` and `Domain`.
   - `Domain` must NOT contain any `Infra` code.
2. **Dependency Injection**:
   - Class instances MUST NOT be initialized automatically within other classes.
   - All dependencies (instances) must be passed as constructor arguments.
   - All central dependency management must occur within `dependencies.py`.

## Code Structure & Conventions
1. **Types**: Every file requiring complex types must have a sibling `*_types.py` file.
2. **Data Structures**: Use `dataclasses` for all `Input`/`Output` objects.
   - Repositories must receive `dataclass` input and return `dataclass` output (e.g., `CreateUserInput`, `CreateUserOutput`).
3. **Encapsulation**:
   - Unnecessary functions must be private (prefixed with `_`).
   - Class constants and variables must be private whenever possible.
4. **Adapters & Mapping**:
   - Each `Adapter` must have a corresponding `*_mappers.py` file in the same directory.
   - Mappers are responsible for translating data between `Infra` and `Domain`.
   - Adapters are strictly tied to specific domain modules and MUST NOT be reused.
5. **Naming**:
   - Domain constructor arguments representing ports should be suffixed with `_port`.

## Testing
1. Every file must have a corresponding unit test file located in `/tests` mirroring the project structure.
2. Unit tests must cover business logic in Domain, mapping logic in Adapters, and repository operations in Infra.
3. Tests MUST be implemented using mocks to isolate components and external dependencies.

## Language
- All code, documentation, and communication must be in English.
- No code comments are allowed.
