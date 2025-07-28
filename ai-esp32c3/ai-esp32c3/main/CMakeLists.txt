# idf_component_register(SRCS "ai-esp32c3.c"
#                     INCLUDE_DIRS ".")

set(SOURCES "app.cpp")
set(INCLUDES ".")

idf_component_register(SRCS ${SOURCES}
                    INCLUDE_DIRS ${INCLUDES})