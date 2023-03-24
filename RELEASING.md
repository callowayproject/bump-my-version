# Releasing

## Setting Requirements

Your requirements are split into parts: dev, prod, and test. They exist in the directory ``requirements``\ . ``Prod`` requirements are required for your app to work properly. ``Dev`` requirements are packages used to help develop this package, which include things for building documentation, packaging the app and generating the changelog. ``Test`` requirements are the libraries required to run tests.

As you develop, you will likely only modify ``requirements/prod.txt``\ .


## Releasing your app

Once you have developed and tested your app, or revisions to it, you need to release new version.

### Deciding the version

First decide how to increase the version. Using `semantic versioning`_:

> Given a version number MAJOR.MINOR.PATCH, increment the:
>
> 1. MAJOR version when you make incompatible API changes,
> 2. MINOR version when you add functionality in a backwards-compatible manner, and
> 3. PATCH version when you make backwards-compatible bug fixes.

This is a judgement call, but here are some guidelines:

1. A database change should be a MINOR version bump at least.
2. If the PATCH version is getting above ``10``\ , as in ``1.0.14``\ , it is acceptable to do a MINOR version.
3. Dropping or adding support of a version of Python or another dependency should be at least a MINOR version.

.. _semantic versioning: https://semver.org/

### Versioning and releasing


Once you've decided how much of a version bump you are going to do, you will run one of three commands:

``make release-patch`` will automatically change the patch version, e.g. ``1.1.1`` to ``1.1.2``\ .

``make release-minor`` will automatically change the minor version, e.g. ``1.1.1`` to ``1.2.0``\ .

``make release-major`` will automatically change the major version, e.g. ``1.1.1`` to ``2.0.0``\ .

Each of these commands do several things:

1. Update the ``CHANGELOG.md`` file with the changes made since the last version, using the Git commit messages.
2. Increments the appropriate version number in the appropriate way.
3. Commits all the changes.
4. Creates a Git tag with the version number.
5. Pushes the repository and tags to the GitHub server.
6. Jenkins recognizes the new tag and publishes the package on PyPI
