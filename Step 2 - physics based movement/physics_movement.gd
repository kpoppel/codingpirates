extends RigidBody2D

# Export variables for easy tweaking
@export var speed = 30
@export var turn_speed = 4

var movement_vector = Vector2()
var prev_angle = 0

# Handle input
func _process(_delta: float) -> void:
	movement_vector = Input.get_vector("Left", "Right", "Forward", "Backward") * speed
	
	var angle = linear_velocity.angle() + PI/2
	if linear_velocity.length_squared() > 0:
		var target_angle = linear_velocity.angle() + PI / 2
		var angle_diff = angle_difference(rotation, target_angle)
		
		if abs(angle_diff) > 0.1: 
			angular_velocity = sign(angle_diff) * turn_speed
		else:
			angular_velocity = 0
	else:
		angular_velocity = 0
	
	
	# Rotate left when left pressed
	#if Input.is_action_pressed("Left"):
		#angular_velocity = -turn_speed
		#
	## Rotate right when right pressed
	#if Input.is_action_pressed("Right"):
		#angular_velocity = turn_speed
	#
	## Drive forward
	#if Input.is_action_pressed("Forward"):
		## Gets a vector pointing forward of length speed * delta
		#movement_vector = Vector2(cos(rotation - PI/2), sin(rotation - PI/2)) * speed
		#
	## Drive backward
	#if Input.is_action_pressed("Backward"):
		## Gets a vector pointing backward of length speed * delta
		#movement_vector = Vector2(cos(rotation + PI/2), sin(rotation + PI/2)) * speed
		#
	## Reset
	#if !Input.is_action_pressed("Forward") and !Input.is_action_pressed("Backward"):
		#movement_vector = Vector2()

# Integrate physics
func _integrate_forces(_state: PhysicsDirectBodyState2D) -> void:
	linear_velocity += movement_vector
