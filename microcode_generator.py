
f = open('generated_microcode', 'w')
f.write("v3.0 hex words addressed\n")

opcode_order = ["LLB","LUB","SR","LR","ALU","SNZ","SZ","SNZ","SC","MR","JMP","JZ","JNZ","JNC","JC","HLT"]
signal = {   "uc_reset" : 1,
                "gate_pc" : 2,
                "load_pc" : 4,
                "bus_read" : 8,
                "bus_write" : 16,
                "mux_ar":32,
                "reg_write_enable" : 64,
                "gate_ar" : 128,
                "mux_reg_pc" : 0,
                "mux_reg_alu_out" : 256,
                "mux_reg_load_lower" : 512,
                "mux_reg_load_upper" : 512 + 256,
                "mux_reg_reg_a" : 1024,
                "set_reg_a_select_to_reg_select" : 2048,
                "gate_ir" : 32768}

micro_preamble = [signal["gate_ar"] + signal["bus_read"],
                  signal["gate_pc"] + signal["gate_ir"]
                  ]

micro_instructions = {
    "LLB": [signal['uc_reset'] + signal["reg_write_enable"]  + signal["mux_reg_load_lower"] + signal["set_reg_a_select_to_reg_select"]
            ],
    "LUB": [signal['uc_reset'] + signal["reg_write_enable"]  + signal["mux_reg_load_upper"] + signal["set_reg_a_select_to_reg_select"]
            ]
    }

def write_instruction(f, ins):
    f.write(" {0:04x}".format(ins))

# max 8 words per opcode
for i,opcode in enumerate(opcode_order):
    if i%2 == 0:
        f.write("{0:02x}:".format(i*8))
    try:
        uc_ops = micro_preamble + micro_instructions[opcode]
    except KeyError:
        uc_ops = micro_preamble

    if len(uc_ops) <8:  # extend with zeros
        uc_ops += (8-len(uc_ops)) * [0]

    for op in uc_ops:
        write_instruction(f, op)

    if i%2 == 1:
        f.write("\n")
f.close()
