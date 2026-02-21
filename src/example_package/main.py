import cadquery as cq

def build_model():
    # Parameters (mm)
    ID = 75.0
    wall = 2.0
    H = 20.0
    bottom = 2.0

    R_in = 0.8      # inner bottom radius
    R_out = 1.0     # outer bottom radius

    R_top_out = 0.9 # outer rim radius (leading edge)
    R_top_in  = 0.9 # inner rim radius (leading edge)

    IR = ID / 2.0
    OR = IR + wall

    # Guard checks (avoid self-intersections)
    if R_in >= min(bottom, wall):
        raise ValueError("R_in must be smaller than bottom and wall thickness.")
    if R_out >= wall:
        raise ValueError("R_out should be smaller than wall thickness.")
    if R_top_out >= wall:
        raise ValueError("R_top_out should be smaller than wall thickness.")
    if R_top_in >= wall:
        raise ValueError("R_top_in should be smaller than wall thickness.")
    if (R_top_out + R_top_in) >= wall:
        raise ValueError("R_top_out + R_top_in must be smaller than wall thickness.")

    wp = cq.Workplane("XZ")

    # Build profile with bottom radii + top rim radii
    profile = (
        wp
        .moveTo(0, 0)

        # bottom to outer corner (leaving room for bottom outer radius)
        .lineTo(OR - R_out, 0)
        .radiusArc((OR, R_out), -R_out)

        # outer wall up, stop short for top outer radius
        .lineTo(OR, H - R_top_out)
        .radiusArc((OR - R_top_out, H), -R_top_out)

        # top face inward, stop short for top inner radius
        .lineTo(IR + R_top_in, H)
        .radiusArc((IR, H - R_top_in), -R_top_in)

        # inner wall down to inner-bottom radius start
        .lineTo(IR, bottom + R_in)
        .radiusArc((IR - R_in, bottom), R_in)

        # inner floor back to axis
        .lineTo(0, bottom)
        .close()
    )

    part = profile.revolve(360, (0, 0, 0), (0, 1, 0))
    
    filename = f"slip_on_cap_{ID}".replace(".", "_")

    cq.exporters.export(part, f"{filename}.step")
    cq.exporters.export(part, f"{filename}.stl")
    return part


if __name__ == "__main__":
    part = build_model()
    show_object(part)