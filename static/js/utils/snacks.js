//@ts-check

const Snackbar = globalThis.Snackbar

/**
 * @param {string} backgroundColor 
 * @param {string} textColor 
 */
function snack(backgroundColor, textColor) {
    /**
     * @param {string} text 
     * @param {Function|null} callback
     */
    const snackFn = function(text, callback = null) {
        Snackbar.show({
            pos: 'bottom-right',
            
            text,
            textColor,
            backgroundColor,
            actionColor: textColor,

            showAction: !!callback,
            onActionClick: callback
        })
    }

    return snackFn
}

export const snackDanger = snack('var(--error)', 'var(--on-error)')
export const snackPrimary = snack('var(--primary)', 'var(--on-primary)')