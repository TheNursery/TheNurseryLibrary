{-# LANGUAGE OverloadedStrings #-}
-----------------------------------------------------------------------------
--
-- Module      :  Server
-- Copyright   :  (c) William Woodhead
-- License     :  MIT
--
-- Maintainer  :  William Woodhead <w.woodhead@soton.ac.uk>
-- Stability   :  alpha
-- Portability :
--
-- | Main server
--
-----------------------------------------------------------------------------

-- | Main entry point to the application.
module Main (
        main
    ) where

import Data.Text (Text)
import Control.Exception (finally)
import Control.Monad (forM_, forever)
import Control.Concurrent (MVar, newMVar, modifyMVar_, modifyMVar, readMVar, forkIO)
import Control.Monad.IO.Class (liftIO)
import Text.Printf

import qualified Data.Text as T
import qualified Data.Text.IO as T
import qualified Data.Map as M

import qualified Network.WebSockets as WS

import DataTypes

-- | Send a message to all connected clients
broadcast :: Text -> ServerState -> IO ()
broadcast msg clients = do
    T.putStrLn msg
    forM_ clients $ \(_, conn) -> WS.sendTextData conn msg

newServerState :: ServerState
newServerState = []

newGameState :: GameState
newGameState = GameState {
        gWidth = 800
    ,   gHeight = 500
    ,   gScoreRadiant = 0
    ,   gScoreDire = 0
    ,   gPhysObjsTable = M.fromList [("ball", PhysObj{ poPos=(400, 250), poVel=(5,5), poDim=(10,10), poDoF=[Horizontal,Vertical] })]
    ,   gBallKey = "ball"
    ,   gMap = Default
    ,   gMinPlayers = 2
    ,   gMaxPlayers = 2
    ,   gNumPlayers = 0
    }

-- | The main entry point.
main :: IO ()
main = do
    putStrLn "Starting GR_Pong.hs server... on port 1234"
    sState <- newMVar newServerState
    gState <- newMVar newGameState
    WS.runServer "0.0.0.0" 1234 $ application sState gState
    putStrLn "Done"

-- | Handles incoming connections
application :: MVar ServerState -> MVar GameState -> WS.ServerApp
application sStateMVar gStateMVar pending = do
    conn <- WS.acceptRequest pending
    msg <- WS.receiveData conn >>= return . T.lines
    sState <- liftIO $ readMVar sStateMVar
    gState <- liftIO $ readMVar gStateMVar
    case head msg of
        _   | (head msg) == "join" -> do if clientExistsByName (T.unpack $ msg !! 1) sState
                                            then WS.sendTextData conn nameErr
                                            else flip finally disconnect $ do
                                                    putStrLn "New client joining"
                                                    let user = T.unpack $ msg !! 1
                                                        team = (read $ T.unpack $ msg !! 2) :: Team
                                                    if team == Spectator
                                                       then let client = (Player{ pUser = user, pTeam = Spectator, pReady = True, pMCol = Nothing, pPhys = [] }, conn)
                                                            in do modifyMVar_ sStateMVar (return . addClient client)
                                                                  WS.sendTextData conn doneMsg
                                                                  broadcastPlayers sStateMVar gStateMVar
                                                                  talk conn sStateMVar gStateMVar client
                                                       else do let pBarPos = if team == Radiant
                                                                              then (fromIntegral 0, fromIntegral $ ((gHeight gState) `div` 2) - 50)
                                                                              else (fromIntegral $ gWidth gState - 25, fromIntegral $ (gHeight gState `div` 2) - 50)
                                                                   pBarKey = "player_" ++ user
                                                                   pBar = PhysObj{ poPos = pBarPos, poVel = (0, 0), poDim = (25, 100), poDoF = [Vertical] }
                                                                   client = (Player{ pUser = user, pTeam = team,
                                                                                     pReady = False, pMCol = Just (read $ T.unpack (msg !! 3)),
                                                                                     pPhys = [pBarKey]}, conn)
                                                                   gState' = gState{gPhysObjsTable = M.insert pBarKey pBar (gPhysObjsTable gState)}
                                                               modifyMVar_ sStateMVar (return . addClient client)
                                                               modifyMVar_ gStateMVar (return . const gState')
                                                               WS.sendTextData conn doneMsg
                                                               broadcastPlayers sStateMVar gStateMVar
                                                               talk conn sStateMVar gStateMVar client

            | otherwise -> do T.putStrLn $ T.concat ["Unknown command: ", head msg]
                              WS.sendTextData conn unknownErr
            where nameErr = "{'error': 'NameError', 'msg': 'Name already taken'}" :: Text
                  unknownErr = "{'error': 'UnknownError', 'msg': 'Unknown command'}" :: Text
                  doneMsg = "{'code': 200, msg: 'OK'}" :: Text
                  disconnect = do
                       --Remove the client and return a new state
                       modifyMVar_ sStateMVar (return . removeClientByName (T.unpack $ msg !! 1))
    putStrLn "Application close"


broadcastPlayers :: MVar ServerState -> MVar GameState -> IO ()
broadcastPlayers sStateMVar gStateMVar = do
    sState <- readMVar sStateMVar
    gState <- readMVar gStateMVar
    let playersJSON = printf "{'players': %s}" (playerListJSON $ map fst sState)
    broadcast (T.pack playersJSON) sState

talk :: WS.Connection -> MVar ServerState -> MVar GameState -> Client -> IO ()
talk conn sStateMVar gStateMVar (player,_) = forever $ do
    msg <- WS.receiveData conn :: IO Text
    liftIO $ do sState <- readMVar sStateMVar
                gState <- readMVar gStateMVar
                putStr $ "Received from client " ++ (pUser player) ++ ": "
                T.putStrLn msg
                WS.sendTextData conn ("Hello, World!" :: Text)
