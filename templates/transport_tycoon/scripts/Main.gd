extends Node2D
@onready var title=$UI/Title
@onready var info=$UI/Info
func _ready():
  if FileAccess.file_exists("res://game_spec.json"):
    var f=FileAccess.open("res://game_spec.json", FileAccess.READ)
    var s=JSON.parse_string(f.get_as_text()); f.close()
    if s and s.has("title"): title.text=str(s["title"])
    info.text="Ressources: "+(", ".join(s.get("resources", [])) if s else "")
