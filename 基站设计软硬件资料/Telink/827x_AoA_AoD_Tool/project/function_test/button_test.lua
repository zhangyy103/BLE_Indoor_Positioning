print("LUA Version: ".._VERSION)
print("lua begin:")
tl_form_draw_ratangle(0,0,600,400,0xffffff,0xffffff)
tl_form_show(0,0,600,400)
tl_button_show(0,10,100,32,"btn 1",1)
tl_button_show(0,40,100,32,"btn 2",2)
tl_edit_show(220,10,100,32,"edit1","default",1)
tl_edit_show(220,40,100,32,"para2","hello",2)
result_tbl = {};
idx=1
for loop = 1,100 do


	result_tbl,btn_idx = tl_message_get();
	tl_form_draw_ratangle(0,0,600,400,0xffffff,0xffffff)

	if btn_idx == 1 then
	  tl_form_draw_text(10,150,"button 1 click!!",25,0xff0000)
	  tl_form_draw_text(10,300,string.format("edit1:%s",result_tbl[1]),25,0x00ff00)
	end

	if btn_idx == 2 then
	  tl_form_draw_text(10,150,"button 2 click!!",25,0xff0000)
	  tl_form_draw_text(10,300,string.format("edit2:%s",result_tbl[2]),25,0x00ff00)
	end

	if btn_idx>100 then
	 break
	 
	end

end 




