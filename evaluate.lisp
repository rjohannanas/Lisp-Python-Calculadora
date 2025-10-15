;; evaluate.lisp

(defun evaluar-expresion (entrada)
  (eval (read-from-string entrada)))

(format t "Ejecutando Lisp...~%")

(let ((args (cdr sb-ext:*posix-argv*))) ; Ignora "sbcl" y "evaluate.lisp"
  (if args
      (let ((entrada (car args)))
        (let ((resultado (evaluar-expresion entrada)))
          (format t "Resultado: ~a~%" resultado)))
      (format t "Uso: sbcl --script evaluate.lisp \"(expresion)\"~%")))
