with import <nixpkgs> {};
(python38.withPackages (p: [p.numpy p.matplotlib])).env
