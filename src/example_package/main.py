"""Provide an exemplary entry point."""

import cadquery as cq


def build_model():

    # =========================
    # Parameter (mm)
    # =========================
    ID = 75.0          # Innendurchmesser
    wall = 2.0         # Wandstärke
    H = 20.0           # Gesamthöhe
    R_in = 0.8         # Innenradius (Boden/Seitenwand)
    bottom = 2.0       # Bodenstärke (du kannst hier auch z.B. 2.0 lassen)

    IR = ID / 2
    OR = IR + wall

    solid = cq.Workplane("XY").circle(OR).extrude(H)

    cavity = (
        cq.Workplane("XY")
        .workplane(offset=bottom)
        .circle(IR)
        .extrude(H - bottom + 0.5)  # ensure it fully cuts
    )

    part = solid.cut(cavity)

    # --- robust fillet selection: bottom face of the cavity ---
    # pick the planar face at z=bottom that is INSIDE the part, then fillet its edges
    part = (
        part.faces(">Z")  # stabilize selection context
            .faces(cq.selectors.NearestToPointSelector((0, 0, bottom + 0.01)))  # face near cavity bottom
            .edges()
            .fillet(R_in)
    )

    cq.exporters.export(part, "slip_on_cap.step")
    cq.exporters.export(part, "slip_on_cap.stl")
