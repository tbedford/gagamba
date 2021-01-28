import resource

soft, hard = resource.getrlimit(resource.RLIMIT_STACK)
print("soft limit stack: %s" % soft)
print("hard limit stack: %s" % hard)
