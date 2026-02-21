import argparse
import cadquery as cq

def build_part(ID: float, wall: float, H: float):
    R_in = 0.8      # inner bottom radius
    R_out = 1.0     # outer bottom radius

    R_top_out = 0.9 # outer rim radius (leading edge)
    R_top_in  = 0.9 # inner rim radius (leading edge)

    IR = ID / 2.0
    OR = IR + wall

    # Guard checks (avoid self-intersections)
    if R_in >= wall:
        raise ValueError("R_in must be smaller than wall thickness.")
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
        .lineTo(IR, wall + R_in)
        .radiusArc((IR - R_in, wall), R_in)

        # inner floor back to axis
        .lineTo(0, wall)
        .close()
    )

    part = profile.revolve(360, (0, 0, 0), (0, 1, 0))
    
    return part


def parse_args() -> tuple[float, float, float]:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate a parametric slip-on lens cap (CadQuery)"
    )

    parser.add_argument(
        "--id",
        type=float,
        default=75.0,
        help="Inner diameter in mm (default: 75.0)",
    )

    parser.add_argument(
        "--wall",
        type=float,
        default=2.0,
        help="Wall thickness in mm (default: 2.0)",
    )

    parser.add_argument(
        "--height",
        type=float,
        default=20.0,
        help="Total height in mm (default: 20.0)",
    )

    args = parser.parse_args()
    
    return args.id, args.wall, args.height

def main():
    
    ID, wall, height = parse_args()
    part = build_part(ID, wall, height)
    
    filename = f"slip-on-cap-{ID}".replace(".", "_")

    cq.exporters.export(part, f"{filename}.step")
    cq.exporters.export(part, f"{filename}.stl")
if __name__ == "__main__":
    main()
