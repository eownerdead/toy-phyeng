{
  inputs = {
    nixpkgs.url = "nixpkgs/nixos-unstable";
    utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, utils }: utils.lib.eachDefaultSystem (system:
    let
      pkgs = import nixpkgs { inherit system; };
    in
    {
      devShells.default = pkgs.mkShell {
        packages = with pkgs; [
          python3
          mypy
          yapf
        ] ++ (with pkgs.python3Packages; [
          flake8
          isort
          toml # required by yapf
          pygame
        ]);
      };
    });
}
