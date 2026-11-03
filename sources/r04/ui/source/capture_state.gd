extends SceneTree
func _initialize() -> void:
	call_deferred("run")
func v(p: Vector2) -> Array:
	return [p.x,p.y]
func common(f: Fighter) -> Dictionary:
	return {"class":f.get_class(),"title":f.title,"position":v(f.position),"health":f.health,"max_health":f.max_health,"cd_one":f.cd_one,"cd_two":f.cd_two,"action":f.action,"visible":f.visible}
func run() -> void:
	var a:=BattleArena.new()
	root.add_child(a)
	a.setup(3103,[2,3])
	var sample := {}
	for step in 2400:
		var fish_hp_before: float = a.heroes[0].health
		a.step(1.0/120.0)
		var largest := 0
		for b in a.bubbles:
			largest=maxi(largest,b.level)
		var sheep: ElectricSheep=a.heroes[1]
		if a.bubbles.size()>=3 and largest>=2 and sheep.wool_active and sheep.charge>=10 and (sheep.health<110 or a.heroes[0].health<110) and not a.finished:
			sample={"source":"actual headless fixed-step simulation, not live gameplay screenshot","seed":3103,"roster":[2,3],"simulation_time":a.simulation_time,"fish":common(a.heroes[0]),"sheep":common(sheep),"bubbles":[],"wool_active":sheep.wool_active,"wool_position":v(sheep.wool_position),"charge":sheep.charge,"zapping":sheep.zapping,"fish_hp_before_step":fish_hp_before,"fish_ordinary_hp_decreased":a.heroes[0].health<fish_hp_before,"baseline_commit":"3134f2b8dd0fe250b01e1e7d3c829da5c54aaa47"}
			for b in a.bubbles:
				sample.bubbles.append({"position":v(b.position),"level":b.level,"radius":b.size_radius(),"absorb_left":b.absorb_left,"launch_left":b.launch_left})
			break
	assert(not sample.is_empty())
	var stream=FileAccess.open("/workspace/shared/R04-review/ui/data/shared_sample.json",FileAccess.WRITE)
	stream.store_string(JSON.stringify(sample,"\t"));stream.close()
	a.queue_free()
	await process_frame
	var stress:=BattleArena.new()
	root.add_child(stress)
	stress.setup(3108,[8,9])
	var hard := {}
	for step in 3600:
		stress.step(1.0/120.0)
		var turtle: ShellTurtle=stress.heroes[0]
		var crow: Crow=stress.heroes[1]
		if crow.dummies.size()==2 and not stress.finished:
			hard={"baseline_commit":"3134f2b8dd0fe250b01e1e7d3c829da5c54aaa47","source":"actual headless fixed-step simulation stress sample, not live gameplay screenshot","seed":3108,"roster":[8,9],"simulation_time":stress.simulation_time,"turtle":common(turtle),"crow":common(crow),"turtle_hidden":turtle.action=="hidden","turtle_action_left":turtle.action_left,"shell_position":v(turtle.shell.position),"shell_spin_left":turtle.shell.spin_left,"feather":crow.feather,"dummies":[]}
			for dummy in crow.dummies:
				hard.dummies.append({"position":v(dummy.position),"health":dummy.health,"max_health":dummy.max_health})
			break
	assert(not hard.is_empty())
	stream=FileAccess.open("/workspace/shared/R04-review/ui/data/stress_sample.json",FileAccess.WRITE)
	stream.store_string(JSON.stringify(hard,"\t"));stream.close()
	stress.queue_free()
	await process_frame
	print("REVIEW_SAMPLE PASS primary_time=",sample.simulation_time," bubbles=",sample.bubbles.size()," charge=",sample.charge," stress_time=",hard.simulation_time," dummies=",hard.dummies.size())
	quit()
