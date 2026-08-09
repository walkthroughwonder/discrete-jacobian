import Lake

open Lake DSL

package spliceCollision

require mathlib from git
  "https://github.com/leanprover-community/mathlib4.git" @
  "3dd956ad3d5bc5dbf49ed1875f430add38a742ca"

@[default_target]
lean_lib SpliceCollision
