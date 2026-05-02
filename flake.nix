{
  description = "Set of tools to work with robots with bilateral constraints";

  inputs.gepetto.url = "github:gepetto/nix";

  outputs =
    inputs:
    inputs.gepetto.lib.mkFlakoboros inputs (
      { lib, ... }:
      {
        pyOverrideAttrs.toolbox-parallel-robots = {
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
    );
}
