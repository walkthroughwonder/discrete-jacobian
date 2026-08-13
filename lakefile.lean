import Lake

open Lake DSL

package discreteJacobian where
  version := v!"1.1.0"

require mathlib from git
  "https://github.com/leanprover-community/mathlib4.git" @
  "3dd956ad3d5bc5dbf49ed1875f430add38a742ca"

@[default_target]
lean_lib DiscreteJacobian where
  srcDir := "lean"
  roots := #[`SpliceCollision]
  weakLeanArgs := #["-j1", "-M4096"]
