
{ pkgs, lib, config, inputs, ... }:

let
  system = pkgs.stdenv.system;
  git-hooks = inputs.git-hooks.packages.${system}.git-hooks;
in {
  name = "bump-my-version";

  cachix.enable = false;

  # Languages to include in the environment
  languages = {
    python = {
      enable = true;
      version = "3.12.7";   # Can change to any version of Python for development
      uv = {
        enable = true;
        sync.enable = false;
      };
    };
  };

  # Define global environment variables. Private environment variables should reside in '.envrc.private'
  env = {
    UV_LINK_MODE = "copy";
    UV_PYTHON_PREFERENCE = "only-system";
    UV_PYTHON = "3.12.7";     # Ensure this matches the Python version above
    UV_PYTHON_DOWNLOADS = "never";
  };

  # https://devenv.sh/packages/
  packages = with pkgs; [
    bashInteractive
    just
    uv
    git
    docker
    fish
    pre-commit
  ];

  # Commands which run when the shell is started
  enterShell = ''
    # Python environment setup
    just ready-py

    # Own the local directory
    just own

    # Install the pre-commit hooks
    pre-commit install

    # Run the fish shell instead of bash
    fish --init-command="source .devenv/state/venv/bin/activate.fish"

    # When the command 'exit' is run to exit the fish shell, then the bash shell is run, so exit that
    exit
  '';

  # See full reference at https://devenv.sh/reference/options/
}
