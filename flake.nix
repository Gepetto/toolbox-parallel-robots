{
  description = "Set of tools to work with robots with bilateral constraints";

  inputs = {
    gepetto.url = "github:gepetto/nix";
    flakoboros.follows = "gepetto/flakoboros";
    gazebros2nix.follows = "gepetto/gazebros2nix";
    flake-parts.follows = "gepetto/flake-parts";
    nixpkgs.follows = "gepetto/nixpkgs";
    nix-ros-overlay.follows = "gepetto/nix-ros-overlay";
    systems.follows = "gepetto/systems";
    treefmt-nix.follows = "gepetto/treefmt-nix";
  };

  outputs =
    inputs:
    inputs.flake-parts.lib.mkFlake { inherit inputs; } (
      { lib, ... }:
      {
        systems = import inputs.systems;
        imports = [
          inputs.gepetto.flakeModule
          {
            flakoboros.pyOverrideAttrs.toolbox-parallel-robots = _: _: {
              src = lib.fileset.toSource {
                root = ./.;
                fileset = lib.fileset.unions [
                  ./CMakeLists.txt
                  ./package.xml
                  ./toolbox_parallel_robots
                ];
              };
            };
          }
        ];
      }
    );
}
