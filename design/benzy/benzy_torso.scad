// ===========================================================================
// Benzy — TORSO study (the structural hub). Detailed, interface-driven.
// See TORSO_DESIGN.md for the why/purpose/Anki-way of every feature below.
// Curate via -D:
//   VARIANT = 1 Unibody/Heritage · 2 Service/Modular · 3 Thermal-forward
//   SHOW    = solid | interfaces | section
// +Y = front (face/chin) · -Y = rear (backpack/exhaust) · +Z = up
// ===========================================================================
$fn = 24;
VARIANT = 1;
SHOW    = "solid";

// ---- torso envelope (representative; the hub band of the body) --------------
TW=84; TD=70; TH=46;

// ---- variant table: [R, BP_MODULE, FINS, SEAM] -----------------------------
vt = [ [10,0,0,0],   // 1 Unibody  : soft, flush backpack, hidden seam
       [ 7,1,0,1],   // 2 Service  : crisp, raised backpack module, visible seam
       [ 9,0,1,0] ]; // 3 Thermal  : finned rear heatsink, expressed cooling
V=vt[VARIANT-1]; R=V[0]; BP_MODULE=V[1]; FINS=V[2]; SEAM=V[3];

INTER = (SHOW=="interfaces");
SECT  = (SHOW=="section");

// ---- palette + interface zone colors ---------------------------------------
body=[0.17,0.17,0.20]; tpu=[0.11,0.11,0.13]; bronze=[0.72,0.46,0.22];
zHead=[0.72,0.46,0.22]; zBase=[0.25,0.70,0.40]; zBack=[0.25,0.55,0.92];
zChg=[0.95,0.78,0.25]; zTherm=[0.92,0.35,0.30]; zAcou=[0.70,0.45,0.85];
glass=[0.20,0.55,0.75]; board=[0.16,0.42,0.72]; batt=[0.20,0.62,0.33]; copper=[0.85,0.45,0.2];
function col(norm,zone)= INTER ? zone : norm;

// ---- helpers ---------------------------------------------------------------
module rbox(w,d,h,r){ r=min(r,w/2,d/2,h/2);
  hull() for(x=[-1,1],y=[-1,1],z=[-1,1]) translate([x*(w/2-r),y*(d/2-r),z*(h/2-r)]) sphere(r); }

// ---- additive structure -----------------------------------------------------
module cowl(){            // IF-1 raised front-top cowl that carries the head pivot
  color(col(body,zHead)) translate([0,TD*0.16,TH*0.28]) rbox(TW*0.66,TD*0.5,TH*0.5,R*0.8);
}
module pivot_bosses(){    // IF-1 coaxial head-tilt axle bosses (high + forward)
  color(col(bronze,zHead)) for(s=[-1,1])
    translate([s*(TW*0.34),TD*0.30,TH*0.42]) rotate([0,90,0]) cylinder(h=7,d=13,center=true);
}
module base_bosses(){     // IF-2 corner screw bosses (point down to the base)
  color(col(body,zBase)) for(x=[-1,1],y=[-1,1])
    translate([x*(TW/2-9),y*(TD/2-9),-TH/2-3]) cylinder(h=8,d=9,center=true);
  color(col(bronze,zBase)) for(x=[-1,1]) translate([x*(TW/2-9),0,-TH/2-2]) cylinder(h=6,d=4,center=true); // locating pins
}
module thermal_fins(){    // IF-6 expressed rear heatsink (variant 3)
  if(FINS) color(col(body,zTherm)) for(i=[-3:3])
    translate([i*7,-TD/2-3,-TH*0.05]) cube([2.4,8,TH*0.5],center=true);
}
module backpack_module(){ // IF-3 raised powered rail module (variant 2)
  if(BP_MODULE) color(col(body,zBack)) translate([0,-TD/2-3,0]) rbox(TW*0.5,8,TH*0.62,3);
}

// ---- subtractive features (holes) ------------------------------------------
module holes(){
  translate([0,TD/2,-TH/2]) rotate([45,0,0]) cube([TW+2,17,17],center=true);          // IF-4 chin chamfer
  translate([0,-TD/2+ (BP_MODULE?-1:5),2]) rbox(TW*0.46,16,TH*0.5,3);                  // IF-3 backpack pocket
  for(i=[-2:2]) translate([0,-TD/2+1,-TH*0.28]) translate([i*7,0,0]) rotate([90,0,0]) cylinder(h=10,d=4.4,center=true); // IF-6 rear exhaust grille
  translate([0,-TD/2+1,-TH*0.28]) rotate([90,0,0]) cylinder(h=12,d=26,center=true);    // IF-6 fan bore
  for(s=[-1,1],i=[-2:2]) translate([s*TW/2,i*6,-TH*0.30]) cube([10,3.2,TH*0.22],center=true); // IF-6 side intake louvers
  for(i=[-2:2],j=[-1,1]) translate([i*6,TD/2-1,-TH*0.22+j*6]) rotate([90,0,0]) cylinder(h=10,d=3.2,center=true); // IF-7 speaker grille (front-low)
  for(x=[-1,1],y=[-1,1]) translate([x*(TW/2-9),y*(TD/2-9),-TH/2-3]) cylinder(h=12,d=3.6,center=true); // IF-2 boss bores
  translate([0,0,-TH/2]) rbox(26,16,9,3);                                              // IF-2 harness pass-through
  if(SEAM) translate([0,0,-TH*0.10]) difference(){rbox(TW+1,TD+1,2,R);rbox(TW-3,TD-3,4,R);} // IF-2 visible seam line
}

// ---- post-hole inserts (sit inside cut regions) ----------------------------
module backpack_inserts(){
  yb=-TD/2+(BP_MODULE?-1:5)+6;
  color(col(bronze,zBack)) for(s=[-1,1]) translate([s*7,yb,2]) cylinder(h=2,d=5,center=true);   // pogo power/data
  color(col([0.05,0.05,0.06],zBack)) translate([0,yb,TH*0.14]) cylinder(h=2.5,d=9,center=true); // backpack button
  color(col(glass,zBack)) translate([0,yb,-TH*0.10]) rbox(TW*0.28,2,3,1);                       // status light pipe
}
module charge_pads(){     // IF-4 on the chin chamfer
  color(col([0.95,0.8,0.3],zChg)) for(i=[-1,0,1])
    translate([i*11,TD/2-7,-TH/2+7]) rotate([45,0,0]) cube([7,5,1.6],center=true);
}
module mic_dots(){        // IF-7 mic crown (top corners)
  color(col(bronze,zAcou)) for(x=[-1,1],y=[-1,1]) translate([x*(TW/2-7),y*(TD/2-7),TH/2-1]) cylinder(h=2,d=4,center=true);
}
module flanks(){          // IF-8 soft-touch side panels
  color(col(tpu,[0.5,0.5,0.55])) for(s=[-1,1]) translate([s*(TW/2-1),0,TH*0.08]) rbox(2.5,TD*0.6,TH*0.5,4);
}

// ---- interior (section only) -----------------------------------------------
module interior(){
  color(board) translate([2,4,2]) cube([2.5,TD*0.5,TH*0.6],center=true);   // RK3588S SoM (vertical)
  color([0.16,0.42,0.72]) for(z=[-1,1]) translate([2,4,z*TH*0.28]) rotate([0,90,0]) cylinder(h=8,d=3,center=true); // standoffs
  color(copper) translate([2,-TD*0.18,TH*0.12]) rotate([0,90,0]) cylinder(h=TW*0.4,d=4,center=true); // heatpipe to rear
  color(zAcou) translate([0,TD*0.22,-TH*0.22]) rbox(TW*0.4,10,TH*0.3,3);   // speaker cavity (front-low)
  color(batt) translate([0,0,-TH/2-2]) rbox(TW*0.5,TD*0.4,6,2);            // battery (lives in base, shown at seam)
}

// ---- torso ------------------------------------------------------------------
module torso(){
  difference(){
    union(){
      color(col(body,body)) rbox(TW,TD,TH,R);
      cowl(); pivot_bosses(); base_bosses(); thermal_fins(); backpack_module(); flanks();
    }
    holes();
  }
  backpack_inserts(); charge_pads(); mic_dots();
}

// ---- dispatch ---------------------------------------------------------------
if(SECT) difference(){ union(){ torso(); interior(); }
                       translate([TW/2,TD/2,TH]) cube([TW,TD,TH*3],center=true); }  // cut front-right octant
else torso();
