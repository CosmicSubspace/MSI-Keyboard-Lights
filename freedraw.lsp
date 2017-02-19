(handler "LIGHTS"
  (lambda (data)
    (let* ((r1 (r1: data))
           (g1 (g1: data))
           (b1 (b1: data))
           (r2 (r2: data))
           (g2 (g2: data))
           (b2 (b2: data))
           (r3 (r3: data))
           (g3 (g3: data))
           (b3 (b3: data))
           )

      (on-device 'rgb-3-zone show-on-zone: (list r1 g1 b1) one:)
      (on-device 'rgb-3-zone show-on-zone: (list r2 g2 b2) two:)
      (on-device 'rgb-3-zone show-on-zone: (list r3 g3 b3) three:)
      ))))
      
