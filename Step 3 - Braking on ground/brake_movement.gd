extends RigidBody2D

# Export variables for easy tweaking
@export var speed = 30
@export var turn_speed = 3

var movement_vector = Vector2()

# Handle input
func _process(_delta: float) -> void:
	# Rotate left when left pressed
	if Input.is_action_pressed("Left"):
		angular_velocity = -turn_speed
		
	# Rotate right when right pressed
	if Input.is_action_pressed("Right"):
		angular_velocity = turn_speed
	
	# Drive forward
	if Input.is_action_pressed("Forward"):
		# Gets a vector pointing forward of length speed * delta
		movement_vector = Vector2(cos(rotation - PI/2), sin(rotation - PI/2)) * speed
		
	# Drive backward
	if Input.is_action_pressed("Backward"):
		# Gets a vector pointing backward of length speed * delta
		movement_vector = Vector2(cos(rotation + PI/2), sin(rotation + PI/2)) * speed
		
	# Reset
	if !Input.is_action_pressed("Forward") and !Input.is_action_pressed("Backward"):
		movement_vector = Vector2()
	
	Brake()

# Integrate physics
func _integrate_forces(_state: PhysicsDirectBodyState2D) -> void:
	linear_velocity += movement_vector
	
func Brake():
	var tilemap = $"../Road"
	var tile_coord = tilemap.local_to_map(tilemap.to_local(global_position))
	var tile_data = tilemap.get_cell_tile_data(tile_coord)
	if tile_data:
		var braking_force = tile_data.get_custom_data("Slowdown")
		movement_vector *= (1-braking_force)
