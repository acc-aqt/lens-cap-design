"""Provide an exemplary entry point."""

import cadquery as cq


def build_model():

    # =========================
    # Parameters (mm)
    # =========================
    ID = 75.0          # inner diameter
    wall = 2.0         # wall thickness
    H = 20.0           # total height
    bottom = 2.0       # bottom thickness

    R_in = 0.8         # inner bottom radius
    R_out = 1.0        # outer bottom radius 

    # Guards (avoid impossible geometry)
    if R_in >= min(bottom, wall):
        raise ValueError("R_in must be smaller than bottom and wall thickness.")
    if R_out >= wall:
        raise ValueError("R_out should be smaller than wall thickness (try 0.6–1.2 for wall=2).")

    IR = ID / 2.0
    OR = IR + wall

    wp = cq.Workplane("XZ")

    profile = (
        wp
        # Start on axis at bottom
        .moveTo(0, 0)

        # Bottom outer, stop before corner radius
        .lineTo(OR - R_out, 0)

        # Outer convex radius: (OR - R_out,0) -> (OR, R_out)
        # Use negative radius if it flips (depends on CQ version/orientation)
        .radiusArc((OR, R_out), -R_out)

        # Outer wall up
        .lineTo(OR, H)

        # Top thickness to inner wall
        .lineTo(IR, H)

        # Inner wall down to where inner radius starts
        .lineTo(IR, bottom + R_in)

        # Inner concave radius: (IR, bottom+R_in) -> (IR - R_in, bottom)
        .radiusArc((IR - R_in, bottom), R_in)

        # Inner floor to axis, then close
        .lineTo(0, bottom)
        .close()
    )

    part = profile.revolve(360, (0, 0, 0), (0, 1, 0))

    cq.exporters.export(part, "slip_on_cap.step")
    cq.exporters.export(part, "slip_on_cap.stl")

