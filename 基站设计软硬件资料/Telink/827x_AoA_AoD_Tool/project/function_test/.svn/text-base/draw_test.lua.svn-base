print("LUA Version: ".._VERSION)
print("lua begin:")

tl_form_show(100,0,320,180)
tl_form_draw_ratangle(0,0,300,150,0xffffff,0xffffff)

for loop = 1,100 do
    --tl_form_draw_ratangle(0,0,320,180,0xffffff,0xffffff)
	tl_form_draw_ellipse(0,0,300,150,0x00ffff,0xffffff)
	for i=1,5 do
	  for j=5,1,-1 do
		x1 = (i*24)+(j*14);
		y1 = (j)*14;
		x2 = x1;
		y2 = y1 + 10+math.random(10);
		y1 = 120 - y1;
		y2 = 120 - y2 ;
		a = array.new(20)
		a[1] = x2
		a[2] = y2
		a[3] = x2+11
		a[4] = y2-11
		a[5] = x2+31
		a[6] = y2-11
		a[7] = x1+31
		a[8] = y1-11
		a[9] = x1+20
		a[10] = y1
		a[11] = x2+20
		a[12] = y2
		tl_form_draw_ratangle(x1,y1+1,x2+21,y2,0x00ff00,0x0000ff)
		tl_form_draw_polygon(a,6,0x00ff00,0x0000ff)
		tl_form_draw_line(x2+20,y2,x2+31,y2-11,0x0000ff)
	  
	  
	  end
	
	end
	tl_progress(loop)
   tl_form_draw_text(10,10,"hello",25,0xff0000)
	tl_sleep_ms(20);
end




tl_form_close()
--tl_error(0x01);



