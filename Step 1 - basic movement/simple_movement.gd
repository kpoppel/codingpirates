extends CharacterBody2D

# Export variables for easy tweaking
@export var speed = 300
@export var turn_speed = 0.05

# Integrate physics
func _physics_process(_delta: float) -> void:
	# Rotate left when left pressed
	if Input.is_action_pressed("Left"):
		rotate(-turn_speed)
		
	# Rotate right when right pressed
	if Input.is_action_pressed("Right"):
		rotate(turn_speed)
		
	# Drive forward
	if Input.is_action_pressed("Forward"):
		# Gets a vector pointing forward of length speed * delta
		var movement_vector = Vector2(cos(rotation - PI/2), sin(rotation - PI/2)) * speed
		velocity = movement_vector
		move_and_slide()
		
	# Drive backward
	if Input.is_action_pressed("Backward"):
		# Gets a vector pointing backward of length speed * delta
		var movement_vector = Vector2(cos(rotation + PI/2), sin(rotation + PI/2)) * speed
		velocity = movement_vector
		move_and_slide()
