if (SYSTEMD)
    if (NOT SYSTEMD_SERVICES_INSTALL_DIR)
        find_package(Systemd)
        if (NOT SYSTEMD_FOUND)
            message(
                FATAL_ERROR
                "Could not locate systemd services install dir."
                " Either pass the -DSYSTEMD_SERVICES_INSTALL_DIR=/path/to/systemd/services option"
                " or install systemd pkg-config"
            )
        endif()
    endif()
    set(EXPAND_BINDIR ${CMAKE_INSTALL_FULL_BINDIR})
    configure_file(systemd/universaltorrent-nox@.service.in ${CMAKE_CURRENT_BINARY_DIR}/universaltorrent-nox@.service @ONLY)
    install(FILES "${CMAKE_CURRENT_BINARY_DIR}/universaltorrent-nox@.service"
        DESTINATION ${SYSTEMD_SERVICES_INSTALL_DIR}
        COMPONENT data
    )
endif()

if (GUI)
    install(FILES org.universaltorrent.UniversalTorrent.desktop
        DESTINATION ${CMAKE_INSTALL_DATAROOTDIR}/applications
        COMPONENT data
    )

    install(FILES org.universaltorrent.UniversalTorrent.metainfo.xml
        DESTINATION ${CMAKE_INSTALL_DATAROOTDIR}/metainfo
        COMPONENT data
    )

    install(DIRECTORY menuicons/
        DESTINATION ${CMAKE_INSTALL_DATAROOTDIR}/icons/hicolor
        COMPONENT data
    )

    install(FILES
        ${PROJECT_SOURCE_DIR}/src/icons/universaltorrent-tray.svg
        ${PROJECT_SOURCE_DIR}/src/icons/universaltorrent-tray-dark.svg
        ${PROJECT_SOURCE_DIR}/src/icons/universaltorrent-tray-light.svg
        DESTINATION ${CMAKE_INSTALL_DATAROOTDIR}/icons/hicolor/scalable/status
        COMPONENT data
    )
else()
    install(FILES org.universaltorrent.UniversalTorrent-nox.metainfo.xml
        DESTINATION ${CMAKE_INSTALL_DATAROOTDIR}/metainfo
        COMPONENT data
    )
endif()
