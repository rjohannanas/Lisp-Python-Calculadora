;; evaluate.lisp

(defun ^ (base exp)
  (expt base exp))

(defun evaluar-expresion (entrada)
  (eval (read-from-string entrada)))

(format t "Ejecutando Lisp...~%")

(let ((args (cdr sb-ext:*posix-argv*))) ; Ignora "sbcl" y "evaluate.lisp"
  (if args
      (let ((entrada (car args)))
        (format t "Resultado: ~a~%" (evaluar-expresion entrada)))
      (format t "Uso: sbcl --script evaluate.lisp \"(expresion)\"~%")))
