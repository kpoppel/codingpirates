extends GridContainer

func _ready() -> void:
	var files := DirAccess.get_files_at("res://Step 5 - Main menu and level select/Levels/")
	var i: int = 1
	for file: String in files:
		var button: Button = Button.new()
		add_child(button)
		button.text = str(i)
		button.add_theme_font_size_override("font_size", 48)
		button.custom_minimum_size = Vector2(80, 80)
		button.set_meta("level", load("res://Step 5 - Main menu and level select/Levels/" + file))
		button.pressed.connect(navigate.bind(button.get_meta("level")))

		i += 1

func navigate(level: PackedScene):
	get_tree().change_scene_to_packed(level)
