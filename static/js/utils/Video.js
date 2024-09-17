//@ts-check

export class Video {
    /** @type {HTMLVideoElement} */ #videoEl
    /** @type {MediaStream|null} */ #stream = null
    /** @type {'user'|'environment'} */ #facingMode = 'user'
    /** @type {boolean} */ #streaming = false

    /**
     * @param {HTMLElement|string} elementOrSelector
     * @param {Partial<{ startStreaming: boolean }>} [initOptions]
     */
    constructor(elementOrSelector, initOptions) {
        let element;

        if (elementOrSelector instanceof HTMLElement) {
            element = elementOrSelector
        } else {
            element = document.querySelector(elementOrSelector)
        }

        if (!(element instanceof HTMLVideoElement)) {
            throw new Error('Constructor element must be a video')
        }

        this.#videoEl = element

        const startStreaming = initOptions?.startStreaming ?? false
        
        if (startStreaming) {
            this.startStreaming()
        }
    }

    get streaming() { return this.#streaming }
    get facingMode() { return !this.#streaming ? null : this.#facingMode }
    get mirrored() { return this.#facingMode === 'user' }
    
    get videoElement() { return this.#videoEl }

    /**
     * @returns {Promise<[MediaStream, MediaStreamTrack]>}
     */
    async #getUserVideoStream() {
        if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
            throw new Error('Video.js: Video Stream Not Available. Possible reasons are that you browser is old or you are not in a secure context (https)')
        }

        const stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: this.#facingMode }})
        return [stream, stream.getVideoTracks()[0]]
    }

    /**
     * @param {MediaStreamTrack} track 
     */
    #setFacingModeUsingTrack(track) {
        const facingMode = track.getSettings().facingMode
        if (facingMode === 'environment') {
            this.#facingMode = 'environment'
        } else if (facingMode === 'user') {
            this.#facingMode = 'user'
        } else {
            this.#facingMode = 'user'
        }
    }

    async startStreaming() {
        const [stream, track] = await this.#getUserVideoStream()
        this.#setFacingModeUsingTrack(track)

        this.#videoEl.style.transform = this.mirrored ? 'scaleX(-1)' : ''
        this.#videoEl.srcObject = stream

        this.#stream = stream
        this.#streaming = true
    }

    stopStreaming() {
        if (this.#stream) {
            this.#stream.getTracks().forEach(
                track => track.stop()
            )

            this.#videoEl.srcObject = null
            this.#stream = null
            this.#streaming = false
        }
    }

    async toggleFacingMode() {
        this.stopStreaming()

        this.#facingMode = this.#facingMode === 'user' ? 'environment' : 'user'
        await this.startStreaming()
    }

    /**
     * @param {string} format 
     * @returns {Promise<Blob>}
     */
    async toBlob(format = 'image/png') {
        return new Promise(resolve => {
            const canvas = document.createElement('canvas')
            const context = canvas.getContext('2d')
    
            if (!context) throw new Error('Video.js: Canvas 2D Context is not defined')
    
            // Establece el tamaño del canvas para que coincida con el video
            canvas.width = this.#videoEl.videoWidth;
            canvas.height = this.#videoEl.videoHeight;
    
            const mirrored = this.mirrored

            // Si está mirror, debo invertir la imagen
            if (mirrored) {
                // Invertir el eje X
                context.save()
                context.scale(-1, 1)

                // Dibuja el fotograma del video en el canvas
                context.drawImage(this.#videoEl, -canvas.width, 0, canvas.width, canvas.height);

                // Restaurar el contexto para que no afecte las operaciones futuras
                context.restore()
            }
            else {
                // Dibuja el fotograma del video en el canvas
                context.drawImage(this.#videoEl, 0, 0, canvas.width, canvas.height);
            }

            // Convierte el canvas a Blob (imagen PNG)
            canvas.toBlob(blob => {
                if (blob) {
                    resolve(blob)
                }
                else {
                    throw new Error('Video.js: Blob is not defined')
                }
                
            }, format);
        })
    }

    async open(){
        const img = await this.toBlob()
        const url = URL.createObjectURL(img)
        window.open(url, '_blank')
    }
}