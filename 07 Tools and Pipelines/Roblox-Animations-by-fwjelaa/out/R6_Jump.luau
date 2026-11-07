-- Built by the fwjelaa animation method. Paste into Studio's command bar (View > Command Bar) in
-- Edit mode and press Enter. Creates ServerStorage.Animations["R6_Jump"] (a KeyframeSequence),
-- which the Animation Editor and Moon Animator 2 can open (see GUIDE.md).
local HttpService = game:GetService("HttpService")
local data = HttpService:JSONDecode([==[{"name":"R6_Jump","rig":"R6","props":[],"loop":false,"slides":true,"priority":"Movement","fps":60,"length":15,"root":"HumanoidRootPart","parents":{"Torso":"HumanoidRootPart","Head":"Torso","Right Arm":"Torso","Left Arm":"Torso","Right Leg":"Torso","Left Leg":"Torso"},"keyframes":[{"time":0.0,"poses":{"Torso":{"cf":[0.0,0.0,0.087718,1.0,0.0,0.0,0.0,0.994522,-0.104529,0.0,0.104529,0.994522],"style":"Linear","dir":"In"},"Head":{"cf":[0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.997564,0.069757,0.0,-0.069757,0.997564],"style":"Linear","dir":"In"},"Right Arm":{"cf":[0.0,0.0,0.0,0.694658,-0.712339,-0.100113,0.71934,0.687898,0.096678,0.0,-0.139173,0.990268],"style":"Linear","dir":"In"},"Left Arm":{"cf":[0.0,0.0,0.0,0.809017,0.582065,0.081804,-0.587785,0.801144,0.112593,0.0,-0.139173,0.990268],"style":"Linear","dir":"In"},"Right Leg":{"cf":[0.0,0.0,0.0,0.999391,-0.034878,-0.001218,0.0349,0.998782,0.034878,0.0,-0.0349,0.999391],"style":"Linear","dir":"In"},"Left Leg":{"cf":[0.0,0.0,0.0,0.994522,-0.104465,-0.003648,0.104529,0.993916,0.034708,0.0,-0.0349,0.999391],"style":"Linear","dir":"In"}},"markers":[]},{"time":0.01666,"poses":{"Torso":{"cf":[0.0,0.0,0.14254,1.0,0.0,0.0,0.0,0.999122,-0.04189,0.0,0.04189,0.999122],"style":"Linear","dir":"In"},"Head":{"cf":[0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.997564,0.069757,0.0,-0.069757,0.997564],"style":"Linear","dir":"In"},"Right Arm":{"cf":[0.0,0.0,0.0,0.170536,-0.974299,-0.147168,0.985319,0.169829,0.017448,0.007994,-0.147983,0.988958],"style":"Linear","dir":"In"},"Left Arm":{"cf":[0.0,0.0,0.0,0.372922,0.91449,0.156962,-0.927678,0.370851,0.043401,-0.018519,-0.161795,0.986651],"style":"Linear","dir":"In"},"Right Leg":{"cf":[0.0,0.0,0.0,0.93604,-0.351322,-0.020072,0.351875,0.935063,0.042897,0.003698,-0.047216,0.998878],"style":"Linear","dir":"In"},"Left Leg":{"cf":[0.0,0.0,0.0,0.967583,-0.252188,-0.013605,0.252549,0.966516,0.045443,0.001689,-0.047405,0.998874],"style":"Linear","dir":"In"}},"markers":[]},{"time":0.03333,"poses":{"Torso":{"cf":[0.0,0.0,0.185178,1.0,0.0,0.0,0.0,0.999976,0.006996,0.0,-0.006996,0.999976],"style":"Linear","dir":"In"},"Head":{"cf":[0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.997564,0.069757,0.0,-0.069757,0.997564],"style":"Linear","dir":"In"},"Right Arm":{"cf":[0.0,0.0,0.0,-0.37774,-0.914716,-0.143552,0.92586,-0.371526,-0.068926,0.009714,-0.158945,0.98724],"style":"Linear","dir":"In"},"Left Arm":{"cf":[0.0,0.0,0.0,-0.132649,0.973992,0.183694,-0.990911,-0.126137,-0.046746,-0.022359,-0.188225,0.981871],"style":"Linear","dir":"In"},"Right Leg":{"cf":[0.0,0.0,0.0,0.815144,-0.57812,-0.03629,0.579246,0.813926,0.044695,0.003698,-0.057454,0.998341],"style":"Linear","dir":"In"},"Left Leg":{"cf":[0.0,0.0,0.0,0.931235,-0.363727,-0.022439,0.364415,0.929744,0.052713,0.001689,-0.057265,0.998358],"style":"Linear","dir":"In"}},"markers":[]},{"time":0.05,"poses":{"Torso":{"cf":[0.0,0.0,0.215635,1.0,0.0,0.0,0.0,0.999122,0.041896,0.0,-0.041896,0.999122],"style":"Linear","dir":"In"},"Head":{"cf":[0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.994226,0.107302,0.0,-0.107302,0.994226],"style":"Linear","dir":"In"},"Right Arm":{"cf":[0.0,0.0,0.0,-0.726475,-0.678362,-0.10982,0.687159,-0.715508,-0.125942,0.006857,-0.166957,0.98594],"style":"Linear","dir":"In"},"Left Arm":{"cf":[0.0,0.0,0.0,-0.502816,0.847171,0.171688,-0.864246,-0.489049,-0.117942,-0.015953,-0.207683,0.978066],"style":"Linear","dir":"In"},"Right Leg":{"cf":[0.0,0.0,0.0,0.696602,-0.715867,-0.047757,0.717455,0.69525,0.043428,0.002114,-0.064515,0.997914],"style":"Linear","dir":"In"},"Left Leg":{"cf":[0.0,0.0,0.0,0.89744,-0.440168,-0.029224,0.441136,0.895613,0.057232,0.000981,-0.064254,0.997933],"style":"Linear","dir":"In"}},"markers":[]},{"time":0.06666,"poses":{"Torso":{"cf":[0.0,0.0,0.233909,1.0,0.0,0.0,0.0,0.998026,0.062798,0.0,-0.062798,0.998026],"style":"Linear","dir":"In"},"Head":{"cf":[0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.990653,0.13641,0.0,-0.13641,0.990653],"style":"Linear","dir":"In"},"Right Arm":{"cf":[0.0,0.0,0.0,-0.887045,-0.455352,-0.076203,0.461672,-0.873688,-0.153389,0.003268,-0.171244,0.985223],"style":"Linear","dir":"In"},"Left Arm":{"cf":[0.0,0.0,0.0,-0.70823,0.690089,0.148955,-0.70594,-0.689942,-0.160093,-0.007708,-0.218536,0.975799],"style":"Linear","dir":"In"},"Right Leg":{"cf":[0.0,0.0,0.0,0.615895,-0.785953,-0.054322,0.787828,0.614481,0.041717,0.000592,-0.068489,0.997652],"style":"Linear","dir":"In"},"Left Leg":{"cf":[0.0,0.0,0.0,0.874227,-0.484363,-0.033448,0.485517,0.87219,0.059654,0.000279,-0.068391,0.997659],"style":"Linear","dir":"In"}},"markers":[]},{"time":0.08333,"poses":{"Torso":{"cf":[0.0,0.0,0.24,1.0,0.0,0.0,0.0,0.997564,0.069757,0.0,-0.069757,0.997564],"style":"CubicV2","dir":"InOut"},"Head":{"cf":[0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.987578,0.157128,0.0,-0.157128,0.987578],"style":"Linear","dir":"In"},"Right Arm":{"cf":[0.0,0.0,0.0,-0.946847,-0.316961,-0.054919,0.321683,-0.932503,-0.16419,0.00083,-0.17313,0.984899],"style":"Linear","dir":"In"},"Left Arm":{"cf":[0.0,0.0,0.0,-0.802443,0.581981,0.131845,-0.596726,-0.781876,-0.180524,-0.001975,-0.223535,0.974694],"style":"Linear","dir":"In"},"Right Leg":{"cf":[0.0,0.0,0.0,0.587785,-0.807046,-0.056434,0.809017,0.586353,0.041002,0.0,-0.069757,0.997564],"style":"CubicV2","dir":"InOut"},"Left Leg":{"cf":[0.0,0.0,0.0,0.866025,-0.498782,-0.034878,0.5,0.863916,0.060411,0.0,-0.069757,0.997564],"style":"CubicV2","dir":"InOut"}},"markers":[]},{"time":0.1,"poses":{"Head":{"cf":[0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.985526,0.169523,0.0,-0.169523,0.985526],"style":"Linear","dir":"In"},"Right Arm":{"cf":[0.0,0.0,0.0,-0.961262,-0.27145,-0.047864,0.275637,-0.946658,-0.166921,0.0,-0.173648,0.984808],"style":"CubicV2","dir":"InOut"},"Left Arm":{"cf":[0.0,0.0,0.0,-0.829038,0.544861,0.125791,-0.559193,-0.80779,-0.186493,0.0,-0.224951,0.97437],"style":"CubicV2","dir":"InOut"}},"markers":[]},{"time":0.11666,"poses":{"Head":{"cf":[0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.984808,0.173648,0.0,-0.173648,0.984808],"style":"CubicV2","dir":"InOut"}},"markers":[]},{"time":0.15,"poses":{"Torso":{"cf":[0.0,0.0,0.3,1.0,0.0,0.0,0.0,0.994522,0.104529,0.0,-0.104529,0.994522],"style":"CubicV2","dir":"InOut"},"Right Leg":{"cf":[0.0,0.0,0.0,0.529919,-0.844821,-0.073912,0.848048,0.527903,0.046185,0.0,-0.087156,0.996195],"style":"CubicV2","dir":"InOut"},"Left Leg":{"cf":[0.0,0.0,0.0,0.809017,-0.585549,-0.051229,0.587785,0.805938,0.07051,0.0,-0.087156,0.996195],"style":"CubicV2","dir":"InOut"}},"markers":[]},{"time":0.16666,"poses":{"Right Arm":{"cf":[0.0,0.0,0.0,-0.984808,-0.169854,-0.036104,0.173649,-0.963287,-0.204753,0.0,-0.207912,0.978148],"style":"CubicV2","dir":"InOut"},"Left Arm":{"cf":[0.0,0.0,0.0,-0.898794,0.423434,0.113459,-0.438371,-0.868169,-0.232625,0.0,-0.258819,0.965926],"style":"CubicV2","dir":"InOut"}},"markers":[]},{"time":0.18333,"poses":{"Head":{"cf":[0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.990268,0.139173,0.0,-0.139173,0.990268],"style":"Linear","dir":"In"}},"markers":[]},{"time":0.21666,"poses":{"Head":{"cf":[0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.993533,0.113544,0.0,-0.113544,0.993533],"style":"Linear","dir":"In"}},"markers":[]},{"time":0.23333,"poses":{"Head":{"cf":[0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.99863,0.052336,0.0,-0.052336,0.99863],"style":"Linear","dir":"In"}},"markers":[]},{"time":0.25,"poses":{"Torso":{"cf":[0.0,0.0,0.3,1.0,0.0,0.0,0.0,0.997564,0.069757,0.0,-0.069757,0.997564],"style":"Linear","dir":"In"},"Head":{"cf":[0.0,0.0,0.0,1.0,0.0,0.0,0.0,0.999959,-0.009069,0.0,0.009069,0.999959],"style":"Linear","dir":"In"},"Right Arm":{"cf":[0.0,0.0,0.0,-0.939693,-0.331861,-0.082742,0.34202,-0.91178,-0.227332,0.0,-0.241922,0.970296],"style":"Linear","dir":"In"},"Left Arm":{"cf":[0.0,0.0,0.0,-0.809017,0.562102,0.171852,-0.587785,-0.773667,-0.236534,0.0,-0.292372,0.956305],"style":"Linear","dir":"In"},"Right Leg":{"cf":[0.0,0.0,0.0,0.866025,-0.496273,-0.060935,0.5,0.85957,0.105542,0.0,-0.121869,0.992546],"style":"Linear","dir":"In"},"Left Leg":{"cf":[0.0,0.0,0.0,0.920505,-0.387818,-0.047618,0.390731,0.913644,0.112181,0.0,-0.121869,0.992546],"style":"Linear","dir":"In"}},"markers":[]}]}]==])
local function build(data)
	local kfs = Instance.new("KeyframeSequence")
	kfs.Name = data.name
	kfs.Loop = data.loop
	kfs.Priority = Enum.AnimationPriority[data.priority]
	for _, k in ipairs(data.keyframes) do
		local kf = Instance.new("Keyframe")
		kf.Time = k.time
		local made = {}
		local function poseFor(part)
			if made[part] then return made[part] end
			local p = Instance.new("Pose")
			p.Name = part
			p.Weight = 0 -- placeholder unless keyed below
			p.CFrame = CFrame.identity
			local parent = data.parents[part]
			p.Parent = parent and poseFor(parent) or kf
			made[part] = p
			return p
		end
		for part, pose in pairs(k.poses) do
			local p = poseFor(part)
			p.CFrame = CFrame.new(table.unpack(pose.cf))
			p.EasingStyle = Enum.PoseEasingStyle[pose.style]
			p.EasingDirection = Enum.PoseEasingDirection[pose.dir]
			p.Weight = 1
		end
		for _, m in ipairs(k.markers) do
			local marker = Instance.new("KeyframeMarker")
			marker.Name = m[1]
			marker.Value = m[2]
			marker.Parent = kf
		end
		kf.Parent = kfs
	end
	return kfs
end
local folder = game.ServerStorage:FindFirstChild("Animations") or Instance.new("Folder")
folder.Name = "Animations"
folder.Parent = game.ServerStorage
local old = folder:FindFirstChild(data.name)
if old then old:Destroy() end
local kfs = build(data)
kfs.Parent = folder
print(("Animation %s ready: ServerStorage.Animations.%s (%d keyframes)"):format(data.name, data.name, #data.keyframes))
return kfs
