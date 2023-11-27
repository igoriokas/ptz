
-- local http = require("socket.http")
-- local mp = require("mp")
-- local utils = require("mp.utils")

local base = "http://192.168.0.101/cgi-bin/rpcCommon.cgi?fun="

local pan_speed = 10;
local tilt_speed = 20;
local diag_speed = 10;

function curl_get(msg, url)
    mp.osd_message(msg)
    mp.msg.info("GET: " .. url)
    local command = io.popen('curl -s -o /dev/null -w "%{http_code}" "' .. url .. '"')
    local status_code = command:read('*a')
    command:close()

    if status_code ~= "200" then
        mp.msg.warn('GET ' .. url .. ' failed:', status_code)
    end
end

function on_left(key)
    if key.event == "down" then
        curl_get("move left", base .. "moveLeft&par=" .. pan_speed)
    else
        curl_get("move stop", base .. "moveStop&par=NULL")
    end
end

function on_right(key)
    if key.event == "down" then
        curl_get("move right", base .. "moveRight&par=" .. pan_speed)
    else
        curl_get("move stop", base .. "moveStop&par=NULL")
    end
end

function on_up(key)
    if key.event == "down" then
        curl_get("move up", base .. "moveUp&par=" .. tilt_speed)
    else
        curl_get("move stop", base .. "moveStop&par=NULL")
    end
end

function on_down(key)
    if key.event == "down" then
        curl_get("move down", base .. "moveDown&par=" .. tilt_speed)
    else
        curl_get("move stop", base .. "moveStop&par=NULL")
    end
end

function on_pgup(key)
    if key.event == "down" then
        curl_get("zoom wide", base .. "zoomWide&par=NULL")
    else
        curl_get("zoom stop", base .. "zoomStop&par=NULL")
    end
end

function on_pgdown(key)
    if key.event == "down" then
        curl_get("zoom tele", base .. "zoomTele&par=NULL")
    else
        curl_get("zoom stop", base .. "zoomStop&par=NULL")
    end
end

mp.add_forced_key_binding("LEFT",   nil, on_left,    {repeatable=false, complex=true})
mp.add_forced_key_binding("RIGHT",  nil, on_right,   {repeatable=false, complex=true})
mp.add_forced_key_binding("UP",     nil, on_up,      {repeatable=false, complex=true})
mp.add_forced_key_binding("DOWN",   nil, on_down,    {repeatable=false, complex=true})
mp.add_forced_key_binding("PGUP",   nil, on_pgup,    {repeatable=false, complex=true})
mp.add_forced_key_binding("PGDWN",  nil, on_pgdown,  {repeatable=false, complex=true})

mp.osd_message("loaded my.lua")
