# Flutter + Dart Skill

This skill provides a strict workflow for building and validating Flutter features with tests.

## Standard Task 1: Scaffold a feature module (screen + state + route)

### Required inputs
- Feature name (snake_case and PascalCase forms).
- Target package path (for example `lib/features/<feature_name>/`).
- State management approach (`setState`, `Provider`, `Riverpod`, etc.).
- Navigation entry point and route name.

### Command/snippet workflow
1. Create feature directories:
   ```bash
   FEATURE=profile_settings
   mkdir -p lib/features/$FEATURE/{presentation,state,data}
   ```
2. Create screen scaffold:
   ```bash
   cat > lib/features/$FEATURE/presentation/profile_settings_screen.dart <<'DART'
   import 'package:flutter/material.dart';

   class ProfileSettingsScreen extends StatelessWidget {
     const ProfileSettingsScreen({super.key});

     static const routeName = '/profile-settings';

     @override
     Widget build(BuildContext context) {
       return Scaffold(
         appBar: AppBar(title: const Text('Profile Settings')),
         body: const Center(child: Text('Profile Settings Content')),
       );
     }
   }
   DART
   ```
3. Register route in app router:
   ```dart
   routes: {
     ProfileSettingsScreen.routeName: (_) => const ProfileSettingsScreen(),
   }
   ```
4. Run analyzer formatting checks:
   ```bash
   dart format lib/features/$FEATURE
   flutter analyze
   ```

### Expected output format
- New feature folder with at least one presentation file.
- Route constant and route registration in app navigation.
- Analyzer output with no errors.

### Validation checklist
- [ ] Feature directory structure exists.
- [ ] Screen class compiles and exposes `routeName`.
- [ ] Route wired into app router.
- [ ] `flutter analyze` reports no blocking issues.

## Standard Task 2: Add a widget test for the new screen

### Required inputs
- Screen/widget class name.
- Expected UI elements/text strings.
- Any required dependencies/mocks.
- Test file location under `test/`.

### Command/snippet workflow
1. Create widget test file:
   ```bash
   mkdir -p test/features/profile_settings
   cat > test/features/profile_settings/profile_settings_screen_test.dart <<'DART'
   import 'package:flutter/material.dart';
   import 'package:flutter_test/flutter_test.dart';
   import 'package:my_app/features/profile_settings/presentation/profile_settings_screen.dart';

   void main() {
     testWidgets('renders profile settings title', (tester) async {
       await tester.pumpWidget(
         const MaterialApp(home: ProfileSettingsScreen()),
       );

       expect(find.text('Profile Settings'), findsOneWidget);
       expect(find.text('Profile Settings Content'), findsOneWidget);
     });
   }
   DART
   ```
2. Execute targeted test:
   ```bash
   flutter test test/features/profile_settings/profile_settings_screen_test.dart
   ```
3. Run full test suite (optional but recommended):
   ```bash
   flutter test
   ```

### Expected output format
- Test file under `test/features/<feature>/`.
- Passing test output with executed test count.
- No uncaught exceptions in test logs.

### Validation checklist
- [ ] Test imports correct feature path.
- [ ] `pumpWidget` uses `MaterialApp` or required wrappers.
- [ ] Assertions verify visible UI behavior.
- [ ] Targeted widget test passes.

## Standard Task 3: Add model + JSON serialization and unit tests

### Required inputs
- Data model name and fields.
- JSON schema/example payload.
- Serialization method (`json_serializable` or manual mapping).
- Unit test scenarios (success + edge case).

### Command/snippet workflow
1. Add model class:
   ```bash
   cat > lib/features/profile_settings/data/profile_settings_model.dart <<'DART'
   class ProfileSettingsModel {
     final String displayName;
     final bool marketingEmails;

     const ProfileSettingsModel({
       required this.displayName,
       required this.marketingEmails,
     });

     factory ProfileSettingsModel.fromJson(Map<String, dynamic> json) {
       return ProfileSettingsModel(
         displayName: json['displayName'] as String,
         marketingEmails: json['marketingEmails'] as bool,
       );
     }

     Map<String, dynamic> toJson() => {
           'displayName': displayName,
           'marketingEmails': marketingEmails,
         };
   }
   DART
   ```
2. Add unit test:
   ```bash
   cat > test/features/profile_settings/profile_settings_model_test.dart <<'DART'
   import 'package:flutter_test/flutter_test.dart';
   import 'package:my_app/features/profile_settings/data/profile_settings_model.dart';

   void main() {
     test('serializes and deserializes ProfileSettingsModel', () {
       const model = ProfileSettingsModel(
         displayName: 'Taylor',
         marketingEmails: true,
       );

       final json = model.toJson();
       final parsed = ProfileSettingsModel.fromJson(json);

       expect(parsed.displayName, 'Taylor');
       expect(parsed.marketingEmails, isTrue);
     });
   }
   DART
   ```
3. Run format + tests:
   ```bash
   dart format lib/features/profile_settings test/features/profile_settings
   flutter test test/features/profile_settings/profile_settings_model_test.dart
   ```

### Expected output format
- Model source file and corresponding unit test.
- Passing test output.
- Optional generated files if using code generation.

### Validation checklist
- [ ] JSON keys match expected API contract.
- [ ] `fromJson` and `toJson` round-trip correctly.
- [ ] Unit tests include positive and edge case coverage.
- [ ] Formatter and tests complete successfully.
