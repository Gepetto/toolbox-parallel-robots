{
  cmake,
  lib,
  pkg-config,
  python3Packages,
  stdenv,
}:

stdenv.mkDerivation rec {
  pname = "toolbox-parallel-robots";
  version = "0-unstable-2024-30-09";

  src = lib.fileset.toSource {
    root = ./.;
    fileset = lib.fileset.unions [
      ./CMakeLists.txt
      ./package.xml
      ./toolbox_parallel_robots
    ];
  };

  cmakeFlags = [
    (lib.cmakeBool "BUILD_BENCHMARK" false)
    (lib.cmakeBool "BUILD_DOCUMENTATION" false)
    (lib.cmakeBool "BUILD_EXAMPLES" false)
    (lib.cmakeBool "BUILD_TESTING" false)
    (lib.cmakeBool "GENERATE_PYTHON_STUBS" false)
  ];

  nativeBuildInputs = [
    cmake
    pkg-config
  ];
  propagatedBuildInputs = [ python3Packages.pinocchio ];

  meta = {
    description = "Set of tools to work with robots with bilateral constraints";
    homepage = "https://github.com/gepetto/toolbox-parallel-robots";
    license = lib.licenses.bsd2;
    maintainers = with lib.maintainers; [ nim65s ];
    platforms = lib.platforms.unix;
  };
}
