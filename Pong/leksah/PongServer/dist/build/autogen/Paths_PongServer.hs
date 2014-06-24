module Paths_PongServer (
    version,
    getBinDir, getLibDir, getDataDir, getLibexecDir,
    getDataFileName
  ) where

import qualified Control.Exception as Exception
import Data.Version (Version(..))
import System.Environment (getEnv)
import Prelude

catchIO :: IO a -> (Exception.IOException -> IO a) -> IO a
catchIO = Exception.catch


version :: Version
version = Version {versionBranch = [0,0,0,1], versionTags = []}
bindir, libdir, datadir, libexecdir :: FilePath

bindir     = "/home/will/.cabal/bin"
libdir     = "/home/will/.cabal/lib/PongServer-0.0.0.1/ghc-7.6.3"
datadir    = "/home/will/.cabal/share/PongServer-0.0.0.1"
libexecdir = "/home/will/.cabal/libexec"

getBinDir, getLibDir, getDataDir, getLibexecDir :: IO FilePath
getBinDir = catchIO (getEnv "PongServer_bindir") (\_ -> return bindir)
getLibDir = catchIO (getEnv "PongServer_libdir") (\_ -> return libdir)
getDataDir = catchIO (getEnv "PongServer_datadir") (\_ -> return datadir)
getLibexecDir = catchIO (getEnv "PongServer_libexecdir") (\_ -> return libexecdir)

getDataFileName :: FilePath -> IO FilePath
getDataFileName name = do
  dir <- getDataDir
  return (dir ++ "/" ++ name)
