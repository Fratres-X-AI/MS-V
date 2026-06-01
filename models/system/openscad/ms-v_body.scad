// MS-V parametric body — OpenSCAD source (Tier B/C)
// v3: AN-M8 matched outer envelope (5.7 x 2.5 in)
// Units: mm. Z = long axis
// STATUS: Engineering estimate — NOT VALIDATION

wall_mm = 2.0;
length_mm = 5.7 * 25.4;
diameter_mm = 2.5 * 25.4;
fuze_stack_mm = 28;
fuze_diameter_mm = 42;

body_r = diameter_mm / 2;
fuze_r = fuze_diameter_mm / 2;
body_h = length_mm - fuze_stack_mm;

$fn = 64;

union() {
    cylinder(h = body_h, r = body_r);
    translate([0, 0, body_h])
        cylinder(h = fuze_stack_mm, r = fuze_r);
    for (a = [0:90:270])
        rotate([0, 0, a])
            translate([body_r - 1, 0, body_h * 0.85])
                cylinder(h = 10, r = 3, center = true);
    translate([0, 0, 8])
        cylinder(h = 8, r = 3, center = true);
}
