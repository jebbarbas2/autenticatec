//@ts-check

import { FlaskAImageService } from '../utils/FlaskAImageService.js'
import { State } from '../utils/State.js'
import { Video } from '../utils/Video.js'

const _flaskAImageService = new FlaskAImageService()

const videoUser = new Video('#videoUser')
const FPS = 1

/** @type {number|null} */
let detectorInterval = null

const streamingState = new State(false)
streamingState.addChangeListener(async streaming => {
    if (streaming) {
        await videoUser.startStreaming()
        //detectorInterval = setInterval(() => detect(), 1000/FPS)
    }
    else {
        if (detectorInterval !== null) {
            clearInterval(detectorInterval)
            detectorInterval = null
        }

        videoUser.stopStreaming()
    }
})

async function login() {
    const blob = await videoUser.toBlob()
    _flaskAImageService.a(blob)
}

const btnLogin = document.querySelector('#btnLogin')
if (btnLogin && btnLogin instanceof HTMLButtonElement) {
    btnLogin.addEventListener('click', e => {
        login()
    })
}

const btnFacingModeToggler = document.querySelector('.video-facing-mode-toggler')
if (btnFacingModeToggler && btnFacingModeToggler instanceof HTMLButtonElement) {
    btnFacingModeToggler.addEventListener('click', e => {
        videoUser.toggleFacingMode()
    })
}

document.addEventListener('DOMContentLoaded', e => {
    streamingState.set(true)
})

document.addEventListener('visibilitychange', e => {
    streamingState.set(document.visibilityState === 'visible')
})

Object.assign(window, { videoUser })