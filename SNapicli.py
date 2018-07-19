from SNAPI import SNREST


dev = SNREST()
results = dev.get_record("incident", "active=true^number=INC0193806")
 
