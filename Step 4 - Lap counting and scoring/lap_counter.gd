extends Area2D

var time: float = 0
var counting: bool = false
var lap_counts: int = 0 # Starting at 0 ensures first passover isn't counted

@onready var lap_time_label: Label = $"../CurrentLapTime"
@onready var prev_time_label: Label = $"../PreviousLapTimes"

func GetTime() -> String:
	var text = ""
	var t = time
	
	# Counts minutes
	if t / 60 < 10:
		text += "0"
	text += str(floori(t / 60)) + ":"
	
	t -= floori(t / 60) * 60
	
	# Counts seconds	
	if t < 10:
		text += "0"
	text += str(floori(t)) + ":"
	
	t -= floori(t)
	
	# Counts centiseconds
	if floor((t - floor(t)) * 100) < 10:
		text += "0"
	text += str(floori((t - floor(t)) * 100))
	
	return text

func _process(delta: float) -> void:
	if counting:
		time += delta
	
	var text = "Time: " + GetTime()
	lap_time_label.text = text

func _on_body_entered(_body: Node2D) -> void:
	counting = true

func _on_body_exited(_body: Node2D) -> void:
	if lap_counts != 0:
		prev_time_label.text += str(int(lap_counts)) + ". " + GetTime() + "\n"
		time = 0
		lap_counts += 1
	else:
		lap_counts += 1
