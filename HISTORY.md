# 1.1 (2024-07-05)
## New Features
- object_tree module - function to wait for any object from the provided object names list (#52)
- squishserver module - Add sync and async command execution methods (#54)

## Bugfixes
- report module - Set result context to proper value and fix section results entries to point to proper script lines (#55)

## Improvements
- object_tree - Documentation for multiple functions (#56)

# 1.0.1 (2024-01-18)
## Bugfixes
- squishserver module - fix handling of the host, port, and location of the target squishserver (#48)

# 1.0.0 (2023-09-20)
## New Features
- squishserver module - allows managing squishservers and (un)registering AUTs directly from your tests (#18)
- object_tree module - introduces a seamless object tree navigation and search capabilities (#28)
- Comprehensive documentation [(https://squape.cyberalpaca.com)](https://squape.cyberalpaca.com) for the Squape module is now available to help you make the most of its features

## Improvements
- squishtest support - Squape can be used togather with squishtest module now (#33)

# 0.2.2 (2023-05-21)
## Bugfixes
- Fixed activating log level support for some Squish test functions (#27)
- Fixed setting initial `LOGLEVEL` to 'LOG' (#29)

# 0.2.1 (2023-05-17)
## Bugfixes
- Fixed a bug with setting log level via `set_level()`(#24)

# 0.2.0 (2023-05-03)
## New Features
- settings module - makes using various test settings easier and cleaner (#7)
- video module - adds features to enhance the video capture capabilities of Squish (#16)
## Improvements
- `LOGLEVEL` of the **report** module can be set with a setter method that accepts also strings (#20)
## Bugfixes
- Fixed a bug where Squish snoozeFactor set to 0 broke the object highlighting when `vph_property()` was used (#15)
- Fixed a bug with nested object properties in `vph_property()` (#14)

# 0.1.0 (2023-04-17)
Initial version of the Python package that extends Squish Python API. It provides tools for everyday automated test cases development.
## Dependencies
- Squish 6.7.0+
## New Features
- report module - adds features to enhance the reporting capabilities of Squish
- vps module - extension of Squish verification points
