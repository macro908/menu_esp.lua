local ScreenGui = Instance.new("ScreenGui")
ScreenGui.Name = "ESPMenuGui"
ScreenGui.Parent = game.CoreGui

local Frame = Instance.new("Frame")
Frame.Size = UDim2.new(0, 200, 0, 120)
Frame.Position = UDim2.new(0, 50, 0, 100)
Frame.BackgroundColor3 = Color3.fromRGB(30, 30, 30)
Frame.Parent = ScreenGui

local ButtonESP = Instance.new("TextButton")
ButtonESP.Size = UDim2.new(1, 0, 0, 50)
ButtonESP.Position = UDim2.new(0, 0, 0, 10)
ButtonESP.BackgroundColor3 = Color3.fromRGB(60, 60, 60)
ButtonESP.TextColor3 = Color3.fromRGB(255, 255, 255)
ButtonESP.Text = "ESP Aç/Kapat"
ButtonESP.Parent = Frame

local espOn = false
local highlights = {}

local function toggleESP()
    espOn = not espOn
    if espOn then
        for _, player in pairs(game.Players:GetPlayers()) do
            if player ~= game.Players.LocalPlayer and player.Character and player.Character:FindFirstChild("HumanoidRootPart") then
                local highlight = Instance.new("Highlight")
                highlight.Adornee = player.Character
                highlight.FillColor = Color3.fromRGB(255, 0, 0)
                highlight.OutlineColor = Color3.fromRGB(255, 255, 255)
                highlight.Parent = player.Character
                table.insert(highlights, highlight)
            end
        end
    else
        for _, hl in pairs(highlights) do
            hl:Destroy()
        end
        highlights = {}
    end
end

ButtonESP.MouseButton1Click:Connect(toggleESP)
