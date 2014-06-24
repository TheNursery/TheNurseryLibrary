-----------------------------------------------------------------------------
--
-- Module      :  DataTypes
-- Copyright   :  (c) William Woodhead
-- License     :  MIT
--
-- Maintainer  :  William Woodhead <w.woodhead@soton.ac.uk>
-- Stability   :  alpha
--
-- | Data types and associated functions used by the GR_Pong.hs server
--
-----------------------------------------------------------------------------

module DataTypes (
        Team(..)
    ,   PhysFreedom(..)
    ,   PhysObj(..)
    ,   PhysTableKey(..)
    ,   GameState(..)
    ,   Colour(..)
    ,   Player(..)
    ,   GameMap(..)
    ,   Client(..)
    ,   ServerState(..)
    ,   Elasticity
    , isPlayer, isSpectator, numPlayers, numSpectators, numClients
    , clientExistsByName, clientExists, addClient, removeClientByName
    , colourToHex, playerToJSON, gameStateToJSON, playerListJSON
    , serverPlayersJSON, physicsTick
    ) where

import Control.Monad (sequence, liftM)
import Data.Map ((!))
import Data.List (intercalate)
import Data.Maybe (fromJust)
import Text.Printf
import qualified Data.Map as M
import qualified Network.WebSockets as WS (Connection)

-- Team tracket object
data Team = Radiant
          | Dire
          | Spectator
          deriving (Show, Ord, Eq, Read)

-- Restrictions on PhysObj movement
data PhysFreedom = Horizontal
                 | Vertical
                 | None
                 deriving (Show, Eq, Ord)

-- A physics rectangle
data PhysObj = PhysObj {
        poPos :: (Double, Double) -- Position in 2D space
    ,   poVel :: (Double, Double) -- Velocity to update position
    ,   poDim :: (Double, Double) -- Dimensions of object in 2-space
    ,   poDoF :: [PhysFreedom]
    } deriving (Show, Eq)


type PhysTableKey = String
type PhysTable = M.Map PhysTableKey PhysObj
type Elasticity = Double

data GameState = GameState {
        gWidth         :: Int -- Width of the game board (in px)
    ,   gHeight        :: Int -- Height of the game board (in px)
    ,   gScoreRadiant  :: Int
    ,   gScoreDire     :: Int
    ,   gPhysObjsTable :: PhysTable
    ,   gBallKey       :: PhysTableKey
    ,   gMap           :: GameMap
    ,   gMinPlayers    :: Int
    ,   gMaxPlayers    :: Int
    ,   gNumPlayers    :: Int
    } deriving (Show, Eq)

data Colour = HotPink
            | OrangeRed
            | SkyBlue
            | Lime
            | Magenta
            deriving (Show, Eq, Read)

data Player = Player {
        pUser  :: String
    ,   pTeam  :: Team
    ,   pPhys  :: [PhysTableKey]
    ,   pMCol  :: Maybe Colour
    ,   pReady :: Bool
    } deriving (Show, Eq)

data GameMap = Default
             deriving (Show, Eq)

type Client = (Player, WS.Connection)
type ServerState = [Client]

-----------------------------------------------------------------------

isPlayer :: Player -> Bool
isPlayer = (/= Spectator) . pTeam

isSpectator :: Player -> Bool
isSpectator = (== Spectator) . pTeam

numPlayers :: ServerState -> Int
numPlayers = length . filter (isPlayer . fst)

numSpectators :: ServerState -> Int
numSpectators = length . filter (isSpectator . fst)

numClients :: ServerState -> Int
numClients = length

clientExistsByName :: String -> ServerState -> Bool
clientExistsByName uname = any ((== uname) . pUser . fst)

clientExists :: Client -> ServerState -> Bool
clientExists = clientExistsByName . pUser . fst

addClient :: Client -> ServerState -> ServerState
addClient c cs = c : cs

removeClientByName :: String -> ServerState -> ServerState
removeClientByName name = filter ( (/= name) . pUser . fst )

colourToHex :: Colour -> String
colourToHex HotPink   = "#FF69B4"
colourToHex OrangeRed = "#FF4500"
colourToHex SkyBlue   = "#87CEEB"
colourToHex Lime      = "#00FF00"
colourToHex Magenta   = "#FF00FF"

playerToJSON :: Player -> String
playerToJSON p = output
    where jsonStrPlayer = "{'username': '%s', 'team':'%s', 'colour': '%s', 'phys_ids': [%s], 'ready': %s}"
          jsonStrSpectator = "{'username': '%s', 'team': '%s'}"
          output = if isSpectator p
                   then printf jsonStrSpectator (pUser p) (show $ pTeam p)
                   else printf jsonStrPlayer (pUser p) (show $ pTeam p) (colourToHex . fromJust . pMCol $ p)
                                             (intercalate "," . map (\s -> "'" ++ s ++ "'") $ pPhys p)
                                             (if pReady p then "true" else "false")

playerListJSON :: [Player] -> String
playerListJSON = (++) "[" . flip (++) "]" . intercalate "," . map playerToJSON

serverPlayersJSON :: ServerState -> String
serverPlayersJSON = playerListJSON . fst . unzip

physObjMapToJSON :: PhysTable -> String
physObjMapToJSON = (++) "[" . flip (++) "]" . intercalate "," . M.foldrWithKey folder []
    where folder k v acc = (printf jsonStr k (fst . poPos $ v) (snd . poPos $ v) (fst . poDim $ v) (snd . poDim $ v)):acc
          jsonStr = "{'id': '%s', 'x': %.2f, 'y': %.2f, 'w': %.2f, 'h': %.2f}"
gameStateToJSON :: GameState -> String
gameStateToJSON gs = printf jsonStr (gWidth gs) (gHeight gs) (gScoreRadiant gs) (gScoreDire gs)
                                    (physObjMapToJSON $ gPhysObjsTable gs) (gBallKey gs) (show $ gMap gs)
                                    (gMinPlayers gs) (gMaxPlayers gs) (gNumPlayers gs)
    where jsonStr = "{'width': %d, 'height': %d, 'score':{'radiant': %d, 'dire': %d}, \
                    \'objects': %s, 'ball_id': '%s', 'map':'%s', 'min_players': %d, 'max_players': %d, 'num_players': %d }"

collisionTime :: PhysObj -> PhysTable -> (Maybe Double, Maybe Double)
collisionTime obj physTable = (minXTime, minYTime)
    where (x1, y1) = poPos obj
          (vx1, vy1) = poVel obj
          (w1, h1) = poDim obj
          -- If obj has Horizontal freedom check for collisions in this direction first
          colTimesFn :: PhysObj -> (Maybe Double, Maybe Double)
          colTimesFn po = (xMin, yMin)
             where  (x2, y2) = poPos po
                    (w2, h2) = poDim po
                    (vx2, vy2) = poVel po
                    xCols = if vx2 /= vx1 then [((x2 - x1) + (w1 + w2))/(vx1 - vx2), ((x2 - x1) - (w1 + w2))/(vy1 - vy2)] else []
                    yCols = if vy2 /= vy1 then [((y2 - y1) + (h1 + h2))/(vy1 - vy2), ((y2 - y1) - (h1 + h2))/(vy1 - vy2)] else []
                    xCols' = filter (\alpha -> alpha >= 0 && alpha <= 1) xCols
                    yCols' = filter (\alpha -> alpha >= 0 && alpha <= 1) yCols
                    xMin = if null xCols' then Nothing else Just (minimum xCols')
                    yMin = if null yCols' then Nothing else Just (minimum yCols')
          (allXTimes, allYTimes) = unzip $ map snd $ M.toList $ M.map colTimesFn physTable
          minXTime = liftM minimum . sequence $ allXTimes
          minYTime = liftM minimum . sequence $ allYTimes

physicsTick :: Elasticity -> PhysTable -> PhysTable
physicsTick e ptable = M.map updater ptable
    where updater :: PhysObj -> PhysObj
          updater po = po { poPos=(x',y'), poVel=(vx', vy') }
            where colTimes = collisionTime po ptable
                  (x, y) = poPos po
                  (vx, vy) = poVel po
                  x'  = maybe (x + vx) (\a -> e * vx * (1 - a)) (fst colTimes)
                  vx' = maybe vx (\_ -> - e * vx) (fst colTimes)
                  y'  = maybe (y + vy) (\a -> e * vy * (1 - a)) (snd colTimes)
                  vy' = maybe vy (\_ -> - e * vy) (snd colTimes)
