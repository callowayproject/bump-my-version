# Contributing to Bump My Version

First off, thanks for taking the time to contribute! ❤️

All types of contributions are encouraged and valued. See the [Table of Contents](#table-of-contents) for different ways to help and details about how this project handles them. Please make sure to read the relevant section before making your contribution. It will make it much easier for us maintainers and smooth out the experience for all involved. The community looks forward to your contributions. 🎉

> If you like the project but don't have time to contribute, that's fine. There are other easy ways to support the project and show your appreciation, which we would also be very happy about:
> - Star the project
> - Tweet about it
> - Refer to this project in your project's readme
> - Mention the project at local meetups and tell your friends/colleagues

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [I Have a Question](#i-have-a-question)
- [Reporting Bugs](#reporting-bugs)
- [Suggesting Enhancements](#suggesting-enhancements)
- [Your First Code Contribution](#your-first-code-contribution)
- [Improving The Documentation](#improving-the-documentation)
- [Styleguides](#styleguides)
- [Join The Project Team](#join-the-project-team)


## Code of Conduct

This project and everyone participating in it are governed by the
[Bump My Version Code of Conduct](https://github.com/callowayproject/bump-my-versionblob/master/CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior
to <coreyoordt@gmail.com>.


## I Have a Question

> If you want to ask a question, we assume that you have read the available [Documentation](https://callowayproject.github.io/bump-my-version/).

Before you ask a question, it is best to search for existing [Issues](https://github.com/callowayproject/bump-my-version/issues) that might help you. In case you have found a suitable issue and still need clarification, you can write your question in this issue. It is also advisable to search the internet for answers first.

If you then still feel the need to ask a question and need clarification, we recommend the following:

- Open an [Issue](https://github.com/callowayproject/bump-my-version/issues/new).
- Provide as much context as you can about what you're running into.
- Provide project and platform versions (nodejs, npm, etc), depending on what seems relevant.

We will then take care of the issue as soon as possible.

## Reporting Bugs

### Before Submitting a Bug Report

A good bug report shouldn't leave others needing to chase you up for more information. Therefore, we ask you to investigate carefully, collect information, and describe the issue in detail in your report. Please complete the following steps in advance to help us fix any potential bug as fast as possible.

- Make sure that you are using the latest version.
- Determine if your bug is really a bug and not an error on your side e.g. using incompatible environment components/versions (Make sure that you have read the [documentation](https://callowayproject.github.io/bump-my-version/). If you are looking for support, you might want to check [this section](#i-have-a-question)).
- To see if other users have experienced (and potentially already solved) the same issue you are having, check if there is not already a bug report existing for your bug or error in the [bug tracker](https://github.com/callowayproject/bump-my-version/issues).
- Also, make sure to search the internet (including Stack Overflow) to see if users outside of the GitHub community have discussed the issue.
- Collect information about the bug:
  - Stack trace (Traceback)
  - OS, Platform, and Version (Windows, Linux, macOS, x86, ARM)
  - The version of Python
  - Possibly your input and the output
  - Can you reliably reproduce the issue? And can you also reproduce it with older versions?


### How Do I Submit a Good Bug Report?

> You must never report security-related issues, vulnerabilities, or bugs that include sensitive information to the issue tracker or elsewhere in public. Instead, sensitive bugs must be sent by email to <coreyoordt@gmail.com>.

We use GitHub issues to track bugs and errors. If you run into an issue with the project:

- Open an [Issue](https://github.com/callowayproject/bump-my-version/issues/new). (Since we can't be sure at this point whether it is a bug or not, we ask you not to talk about a bug yet and not to label the issue.)
- Explain the behavior you would expect and the actual behavior.
- Please provide as much context as possible and describe the *reproduction steps* that someone else can follow to recreate the issue on their own. This usually includes your code. For good bug reports, you should isolate the problem and create a reduced test case.
- Provide the information you collected in the previous section.

Once it's filed:

- The project team will label the issue accordingly.
- A team member will try to reproduce the issue with your provided steps. If there are no reproduction steps or no obvious way to reproduce the issue, the team will ask you for those steps and will not address them until they are included.
- If the team is able to reproduce the issue, the issue will be left to be [implemented by someone](#your-first-code-contribution).


## Suggesting Enhancements

This section guides you through submitting an enhancement suggestion for Bump My Version, **including completely new features and minor improvements to existing functionality**. Following these guidelines will help maintainers and the community to understand your suggestion and find related suggestions.

### Before Submitting an Enhancement

- Make sure that you are using the latest version.
- Read the [documentation](https://callowayproject.github.io/bump-my-version/) carefully and find out if the functionality is already covered, maybe by an individual configuration.
- Perform a [search](https://github.com/callowayproject/bump-my-version/issues) to see if the enhancement has already been suggested. If it has, add a comment to the existing issue instead of opening a new one.
- Find out whether your idea fits with the scope and aims of the project. It's up to you to make a strong case to convince the project's developers of the merits of this feature. Keep in mind that we want features that will be useful to the majority of our users and not just a small subset. If you're just targeting a minority of users, consider writing an add-on/plugin library.

### How Do I Submit a Good Enhancement Suggestion?

Enhancement suggestions are tracked as [GitHub issues](https://github.com/callowayproject/bump-my-version/issues).

- Use a **clear and descriptive title** for the issue to identify the suggestion.
- **Describe the problem or use case** this enhancement solves **or the new benefit** it provides.
- **Explain why this enhancement would be useful** to most Bump My Version users. You may also want to point out the other projects that solved it better and which could serve as inspiration.
- Provide a **step-by-step description of the suggested enhancement** in as many details as possible.
- You may also tell how current alternatives do not work for you, if appropriate

<!-- You might want to create an issue template for enhancement suggestions that can be used as a guide and that defines the structure of the information to be included. If you do so, reference it here in the description. -->

## Your First Code Contribution


> ### Legal Notice
>
> When contributing to this project, you must agree that you have authored 100% of the content, that you have the necessary rights to the content and that the content you contribute may be provided under the project license.

### Setup

There are several ways to create an isolated Python development environment. This is the [default method](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/#creating-a-virtual-environment).

Run the following in a terminal:

```console
# Clone the repository
git clone https://github.com/callowayproject/bump-my-version.git

# Enter the repository
cd bump-my-version

# Create, then activate a virtual environment
python -m venv env
source env/bin/activate

# Install the development requirements
python -m pip install -r requirements/dev.txt
```

### Run tests

Once setup, you should be able to run tests:

```console
pytest
```

### Install Pre-commit Hooks

Pre-commit hooks are scripts that run every time you make a commit. If any of the scripts fail, it stops the commit. You can see a listing of the checks in the ``.pre-commit-config.yaml`` file.

```console
pre-commit install
```

## Improving The Documentation
Please, please help us here.

## Styleguides
### Coding Style

All of the basic coding styles are configured into tools for fixing and checking them. [Pre-commit](https://pre-commit.com) is used to automate the process.

### Commit Messages

**Commit messages are used to generate the change log.**

**New changes**

Commit messages are categorized as "new" if the commit message starts with:

- new
- add

For example: `Added this cool new feature` or `New document type added`.

**Updates**

Commit messages are categorized as "updates" if the commit message starts with:

- update
- change
- rename
- remove
- delete
- improve
- refacto
- chg
- modif

For example: `Modified the taxonomy schema` or `Improves performance by 419%`

**Fixes**

Commit messages are categorizes as "fixes" if the commit message starts with:

- fix

For example: `Fixes bug #123`

**Other**

All other commit messages are categorized as "other."

**Ignoring commit messages**

To have the change log generator ignore this commit, add to the summary line:

- `@minor`
- `!minor`
- `@cosmetic`
- `!cosmetic`
- `@refactor`
- `!refactor`
- `@wip`
- `!wip`

## Join The Project Team

If you would like to be a maintainer, reach out to coreyoordt@gmail.com.

## Attribution
This guide is based on the **contributing-gen**. [Make your own](https://github.com/bttger/contributing-gen)!
