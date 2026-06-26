// ===========================================================================
// Benzy (Vector 3.0) — parametric massing model · CANONICAL machine (no arms/drone)
// Component-modular: base / torso / head / internals / dock are separate modules,
// so we can curate and re-assemble each independently.
// Render with render.sh. Curate via -D overrides:
//   STYLE = 1 Heritage · 2 Rugged · 3 Sleek
//   SHOW  = all | head | base | torso | internals | exploded | dock
// Grounded in the spec: ~105×80×130 mm, tracked base, 1.54" face, mic ring, backpack bay.
// ===========================================================================
$fn = 24;

// ---- curation switches (override with -D) ----
STYLE = 1;
SHOW  = "all";
HEAD_TILT = -6;   // slight downward gaze (deg)

// ---- style table -------------------------------------------------------------
// [RAD, TKH, TKW, HW, HD, HH, BW, BD, TORSOH, BASEH]
styles = [
  [10, 40, 18, 70, 46, 38, 105, 80, 42, 48],   // 1 Heritage  (curvy, Vector-evolved)
  [ 5, 54, 22, 80, 52, 36, 110, 84, 38, 54],   // 2 Rugged    (chunky, big tracks, boxy)
  [15, 36, 15, 66, 44, 48, 100, 76, 46, 42]    // 3 Sleek     (tall, smooth, slim tracks)
];
P=styles[STYLE-1];
RAD=P[0]; TKH=P[1]; TKW=P[2]; HW=P[3]; HD=P[4]; HH=P[5];
BW=P[6]; BD=P[7]; TORSOH=P[8]; BASEH=P[9];

// z-stack (base bottom at z=0)
base_z  = BASEH/2;
torso_z = BASEH + TORSOH/2;
head_z  = BASEH + TORSOH + HH/2;

// ---- palette -----------------------------------------------------------------
charcoal=[0.17,0.17,0.20]; bronze=[0.72,0.46,0.22]; faceblk=[0.04,0.04,0.05];
glass=[0.20,0.55,0.75]; eyecol=[0.25,0.85,0.95];
batt=[0.20,0.62,0.33]; board=[0.15,0.42,0.72]; fanc=[0.30,0.30,0.36];

// ---- helpers -----------------------------------------------------------------
module rbox(w,d,h,r){
  r=min(r,w/2,d/2,h/2);
  hull() for(x=[-1,1],y=[-1,1],z=[-1,1])
    translate([x*(w/2-r), y*(d/2-r), z*(h/2-r)]) sphere(r);
}
module capsule_y(len,dia,wid){            // tank-tread stadium: long axis Y, thickness X
  hull() for(s=[-1,1])
    translate([0, s*(len/2-dia/2), 0]) rotate([0,90,0]) cylinder(h=wid,d=dia,center=true);
}

// ---- components --------------------------------------------------------------
module tracks(){
  off=BW/2-TKW/2; len=BD*0.96;
  color(charcoal) for(s=[-1,1]) translate([s*off,0,TKH/2]) capsule_y(len,TKH,TKW);
  color(bronze)   for(s=[-1,1],y=[-1,1])
    translate([s*(off+TKW/2-1), y*(len/2-TKH/2), TKH/2]) rotate([0,90,0]) cylinder(h=2,d=TKH*0.42,center=true);
}
module drive_base(){
  color(charcoal) translate([0,0,base_z]) rbox(BW-TKW*1.4, BD*0.9, BASEH, RAD);
  tracks();
  color(bronze)   translate([0,0,BASEH-3]) rbox(BW-TKW*1.4+1, BD*0.9+1, 4, 2);   // beltline
}
module torso(){
  color(charcoal) translate([0,0,torso_z]) rbox(BW-TKW*1.2, BD*0.86, TORSOH, RAD);
  // backpack bay (rear -Y): bronze rim + dark inset
  bayw=BW*0.40; bayh=TORSOH*0.48; yb=BD*0.86/2;
  color(bronze)  translate([0,-(yb-1),torso_z]) rbox(bayw+4,3,bayh+4,1.5);
  color(faceblk) translate([0,-(yb-2),torso_z]) rbox(bayw,4,bayh,1.5);
}
module head(){
  translate([0,0,head_z]) rotate([HEAD_TILT,0,0]){
    color(charcoal) rbox(HW,HD,HH,RAD);
    fpw=HW*0.82; fph=HH*0.6; yf=HD/2;
    color(faceblk) translate([0,yf-2,HH*0.02]) rbox(fpw,6,fph,4);          // face plate
    color(glass)   translate([0,yf+1,HH*0.02]) scale([1,0.5,1]) rbox(fpw*0.98,8,fph*0.96,4); // convex lens
    eyw=fpw*0.26; eyh=fph*0.5; eg=fpw*0.16;
    color(eyecol)  for(s=[-1,1]) translate([s*eg,yf+2,HH*0.04]) rbox(eyw,4,eyh,eyw*0.4);      // eyes
    color(bronze)  translate([0,yf-2,HH*0.34]) rbox(HW*0.5,5,7,2.5);       // camera bar
    color(faceblk) for(i=[-1,0,1]) translate([i*HW*0.14,yf+1.5,HH*0.34]) rotate([90,0,0]) cylinder(h=2,d=4,center=true);
    color(bronze)  for(x=[-1,1],y=[-1,1]) translate([x*(HW/2-6),y*(HD/2-6),HH/2-1]) cylinder(h=2,d=4,center=true); // mic ring
  }
}
module internals(a=1){
  color(batt,a)  translate([0,0,BASEH*0.45]) rbox(BW*0.5,BD*0.5,BASEH*0.6,4);    // battery (base)
  color(board,a) translate([0,5,torso_z]) cube([BW*0.5,3,TORSOH*0.8],center=true); // RK3588S SoM
  color(board,a) translate([-BW*0.2,-8,torso_z]) cube([20,3,18],center=true);     // STM32 board
  color(fanc,a)  translate([0,-BD*0.3,torso_z]) rotate([90,0,0]) cylinder(h=8,d=24,center=true); // rear fan
}
module dock(){
  dw=BW*1.1; dd=BD*1.2; dh=26;
  color(charcoal) translate([0,0,dh/2]) rbox(dw,dd,dh,8);
  color(charcoal) translate([0,dd*0.18,dh]) rotate([18,0,0]) rbox(BW*0.8,dd*0.5,5,3);  // cradle ramp
  color(bronze)   translate([0,dd*0.36,dh+3]) rbox(BW*0.4,4,3,1);                       // contacts
  color(faceblk)  translate([0,-dd*0.28,dh+6]) cylinder(h=12,d=26);                     // LiDAR puck
  color(glass)    translate([0,-dd*0.28,dh+12]) cylinder(h=3,d=26);
  color(eyecol)   translate([0,dd*0.42,dh*0.5]) sphere(3);                              // status light
}
module shell_all(){ drive_base(); torso(); head(); }

// ---- dispatch ----------------------------------------------------------------
if      (SHOW=="all")       shell_all();
else if (SHOW=="head")      head();
else if (SHOW=="base")      drive_base();
else if (SHOW=="torso")     torso();
else if (SHOW=="dock")      dock();
else if (SHOW=="internals"){ color(charcoal,0.12) shell_all(); internals(1); }
else if (SHOW=="exploded"){ drive_base(); translate([0,0,42]) torso(); translate([0,0,96]) head(); }
