// MS-V parametric body — OpenSCAD source (Tier B)
// Units: mm. Z = long axis (throw direction when stored vertically in pouch)
// STATUS: Engineering estimate — NOT VALIDATION

wall_mm = 2.0;
length_mm = 7.1 * 25.4;
diameter_mm = 3.1 * 25.4;
fuze_stack_mm = 28;
fuze_diameter_mm = 52;

body_r = diameter_mm / 2;
fuze_r = fuze_diameter_mm / 2;
body_h = length_mm - fuze_stack_mm;

$fn = 64;

union() {
    cylinder(h = body_h, r = body_r);
    translate([0, 0, body_h])
        cylinder(h = fuze_stack_mm, r = fuze_r);
    // emission ports (visual only)
    for (a = [0:90:270])
        rotate([0, 0, a])
            translate([body_r - 1, 0, body_h * 0.85])
                cylinder(h = 12, r = 4, center = true);
    translate([0, 0, 8])
        cylinder(h = 10, r = 4, center = true);
}

// AN-M8 reference (offset for scale compare) — uncomment to preview
// translate([120, 0, 0])
//     cylinder(h = 5.7 * 25.4, r = 2.5 * 25.4 / 2);
