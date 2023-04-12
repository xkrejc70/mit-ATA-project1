#!/usr/bin/env python3
"""
Example of usage/test of Cart controller implementation.
"""

import sys
from cartctl import CartCtl, Status as CStatus
from cart import Cart, CargoReq, Status
from jarvisenv import Jarvis
import unittest

def log(msg):
    "simple logging"
    print('  %s' % msg)

START_TIME = 10
MINUTE = 60

class TestCartRequests(unittest.TestCase):

    def test_happy(self):
        log('== NEW TEST - Happy-path test')

        def add_load(c: CartCtl, cargo_req: CargoReq):
            "callback for schedulled load"
            log('%d: Requesting %s at %s' % \
                (Jarvis.time(), cargo_req, cargo_req.src))
            c.request(cargo_req)

        def on_move(c: Cart):
            "example callback (for assert)"
            # put some asserts here
            log('%d: Cart is moving %s->%s' % (Jarvis.time(), c.pos, c.data))

        def on_load(c: Cart, cargo_req: CargoReq):
            "example callback for logging"
            log('%d: Cart at %s: loading: %s' % (Jarvis.time(), c.pos, cargo_req))
            log(c)
            cargo_req.context = "loaded"

        def on_unload(c: Cart, cargo_req: CargoReq):
            "example callback (for assert)"
            # put some asserts here
            log('%d: Cart at %s: unloading: %s' % (Jarvis.time(), c.pos, cargo_req))
            log(c)
            self.assertEqual('loaded', cargo_req.context)
            cargo_req.context = 'unloaded'
            if cargo_req.content == 'helmet':
                self.assertEqual('B', c.pos)
            if cargo_req.content == 'heart':
                self.assertEqual('A', c.pos)
            #if cargo_req.content.startswith('bracelet'):
            #    self.assertEqual('C', c.pos)
            if cargo_req.content == 'braceletR':
                self.assertEqual('A', c.pos)
            if cargo_req.content == 'braceletL':
                self.assertEqual('C', c.pos)

        # Setup Cart
        # 4 slots, 150 kg max payload capacity, 2=max debug
        cart_dev = Cart(4, 150, 0)
        cart_dev.onmove = on_move

        # Setup Cart Controller
        c = CartCtl(cart_dev, Jarvis)

        # Setup Cargo to move
        helmet = CargoReq('A', 'B', 20, 'helmet')
        helmet.onload = on_load
        helmet.onunload = on_unload

        heart = CargoReq('C', 'A', 40, 'heart')
        heart.onload = on_load
        heart.onunload = on_unload

        braceletR = CargoReq('D', 'A', 40, 'braceletR')
        braceletR.onload = on_load
        braceletR.onunload = on_unload

        braceletL = CargoReq('D', 'C', 40, 'braceletL')
        braceletL.onload = on_load
        braceletL.onunload = on_unload

        # Setup Plan
        Jarvis.reset_scheduler()
        #         when  event     called_with_params
        Jarvis.plan(10, add_load, (c,helmet))
        Jarvis.plan(45, add_load, (c,heart))
        Jarvis.plan(40, add_load, (c,braceletR))
        Jarvis.plan(25, add_load, (c,braceletL))
        
        # Exercise + Verify indirect output
        #   SUT is the Cart.
        #   Exercise means calling Cart.request in different time periods.
        #   Requests are called by add_load (via plan and its scheduler).
        #   Here, we run the plan.
        Jarvis.run()

        # Verify direct output
        log(cart_dev)
        self.assertTrue(cart_dev.empty())
        self.assertEqual('unloaded', helmet.context)
        self.assertEqual('unloaded', heart.context)
        self.assertEqual('unloaded', braceletR.context)
        self.assertEqual('unloaded', braceletL.context)
        #self.assertEqual(cart_dev.pos, 'C')

    def test_case_1(self):
        log('== NEW TEST - Test case 1: normal load')

        def add_load(c: CartCtl, cargo_req: CargoReq):
            "callback for schedulled load"
            log('%d: Requesting %s at %s' % \
                (Jarvis.time(), cargo_req, cargo_req.src))
            c.request(cargo_req)

        def on_move(c: Cart):
            self.assertEqual(Status.Moving, c.status)
            log('%d: Cart is moving %s->%s' % (Jarvis.time(), c.pos, c.data))

        def on_load(c: Cart, cargo_req: CargoReq):
            "example callback for logging"
            log('%d: Cart at %s: loading: %s' % (Jarvis.time(), c.pos, cargo_req))
            log(c)
            cargo_req.context = "loaded"
            self.assertLess(Jarvis.time(), START_TIME + MINUTE)
            self.assertFalse(cargo_req.prio)
            check_cargo_request(cargo_req)
            self.assertIn(cargo_req, c.slots)

        def on_unload(c: Cart, cargo_req: CargoReq):
            "example callback (for assert)"
            log('%d: Cart at %s: unloading: %s' % (Jarvis.time(), c.pos, cargo_req))
            log(c)
            self.assertEqual('loaded', cargo_req.context)
            cargo_req.context = 'unloaded'
            self.assertEqual('B', c.pos)
            self.assertNotIn(cargo_req, c.slots)
            self.assertFalse(cargo_req.prio)

        def check_cart_before(c: Cart):
            self.assertTrue(c.empty())
            self.assertFalse(c.any_prio_cargo())
            self.assertEqual(150, c.load_capacity)
            self.assertEqual(Status.Idle, c.status)

        def check_cart_after(c: Cart):
            self.assertTrue(c.empty())
            self.assertFalse(c.any_prio_cargo())
            self.assertEqual(150, c.load_capacity)
            self.assertEqual(Status.Idle, c.status)

        def check_cargo_request(cargo_req: CargoReq):
            self.assertFalse(cargo_req.prio)
            self.assertEqual('material', cargo_req.content)
            self.assertEqual('A', cargo_req.src)
            self.assertEqual('B', cargo_req.dst)
            self.assertEqual(20, cargo_req.weight)

        # Setup Cart
        cart_dev = Cart(4, 150, 0)
        cart_dev.onmove = on_move

        # Setup Cart Controller
        c = CartCtl(cart_dev, Jarvis)

        # Setup Cargo to move
        material = CargoReq('A', 'B', 20, 'material')
        material.onload = on_load
        material.onunload = on_unload
    
        # Setup Plan
        Jarvis.reset_scheduler()
        Jarvis.plan(5, check_cart_before, (cart_dev,))
        Jarvis.plan(5, check_cargo_request, (material,))
        Jarvis.plan(START_TIME, add_load, (c, material))
        Jarvis.run()

        # Verify direct output
        log(cart_dev)
        check_cart_after(cart_dev)
        self.assertEqual('unloaded', material.context)
        self.assertEqual(CStatus.Idle, c.status)

    def test_case_2(self):
        log('== NEW TEST - Test case 2: not loaded within 1 minute')

        def add_load(c: CartCtl, cargo_req: CargoReq):
            "callback for schedulled load"
            log('%d: Requesting %s at %s' % \
                (Jarvis.time(), cargo_req, cargo_req.src))
            c.request(cargo_req)

        def on_move(c: Cart):
            self.assertEqual(Status.Moving, c.status)
            log('%d: Cart is moving %s->%s' % (Jarvis.time(), c.pos, c.data))

        def on_load(c: Cart, cargo_req: CargoReq):
            "example callback for logging"
            log('%d: Cart at %s: loading: %s' % (Jarvis.time(), c.pos, cargo_req))
            log(c)
            cargo_req.context = "loaded"
            self.assertGreater(Jarvis.time(), START_TIME + MINUTE)
            self.assertTrue(cargo_req.prio)

        # Setup Cart
        cart_dev = Cart(4, 150, 0)
        cart_dev.onmove = on_move

        # Setup Cart Controller
        c = CartCtl(cart_dev, Jarvis)

        # Setup Cargo to move
        material = CargoReq('A', 'B', 20, 'material')
        material.onload = on_load

        # Setup Plan
        Jarvis.reset_scheduler()
        Jarvis.plan(START_TIME, add_load, (c, material))
        Jarvis.run()

        # Verify direct output
        log(cart_dev)

    def test_case_3(self):
        log('== NEW TEST - Test case 3: priority load within 1 minute')
        
        def add_load(c: CartCtl, cargo_req: CargoReq):
            "callback for schedulled load"
            log('%d: Requesting %s at %s' % \
                (Jarvis.time(), cargo_req, cargo_req.src))
            c.request(cargo_req)

        def on_move(c: Cart):
            self.assertEqual(Status.Moving, c.status)
            log('%d: Cart is moving %s->%s' % (Jarvis.time(), c.pos, c.data))

        def on_load(c: Cart, cargo_req: CargoReq):
            "example callback for logging"
            log('%d: Cart at %s: loading: %s' % (Jarvis.time(), c.pos, cargo_req))
            log(c)
            cargo_req.context = "loaded"
            if cargo_req.content == 'material':
                self.assertGreater(Jarvis.time(), START_TIME + MINUTE)
                self.assertTrue(cargo_req.prio)

        def on_unload(c: Cart, cargo_req: CargoReq):
            "example callback (for assert)"
            log('%d: Cart at %s: unloading: %s' % (Jarvis.time(), c.pos, cargo_req))
            log(c)
            self.assertEqual('loaded', cargo_req.context)
            cargo_req.context = 'unloaded'
            self.assertEqual('B', c.pos)
            self.assertNotIn(cargo_req, c.slots)
            self.assertFalse(cargo_req.prio)   

        def check_cartsnt_status(c: CartCtl):
            self.assertEqual(CStatus.UnloadOnly, c.status)

        # Setup Cart
        cart_dev = Cart(4, 150, 0)
        cart_dev.onmove = on_move

        # Setup Cart Controller
        c = CartCtl(cart_dev, Jarvis)

        # Setup Cargo to move
        material = CargoReq('A', 'D', 20, 'material')
        material.onload = on_load
        material.onunload = on_unload
    
        # Setup Plan
        Jarvis.reset_scheduler()
        Jarvis.plan(START_TIME, add_load, (c, material))
        Jarvis.plan(START_TIME + MINUTE, check_cartsnt_status, (c,))
        Jarvis.run()

        # Verify direct output
        log(cart_dev)
        self.assertEqual('unloaded', material.context)

    def test_case_4(self):
        log('== NEW TEST - Test case 4: cancel request')
        
        def add_load(c: CartCtl, cargo_req: CargoReq):
            "callback for schedulled load"
            log('%d: Requesting %s at %s' % \
                (Jarvis.time(), cargo_req, cargo_req.src))
            c.request(cargo_req)

        def on_move(c: Cart):
            self.assertEqual(Status.Moving, c.status)
            log('%d: Cart is moving %s->%s' % (Jarvis.time(), c.pos, c.data))

        def on_load(c: Cart, cargo_req: CargoReq):
            "example callback for logging"
            log('%d: Cart at %s: loading: %s' % (Jarvis.time(), c.pos, cargo_req))
            log(c)
            cargo_req.context = "loaded"
            if cargo_req.content == 'material':
                self.assertGreater(Jarvis.time(), START_TIME + MINUTE + MINUTE)  

        def check_cartsnt_status(c: CartCtl):
            self.assertEqual(CStatus.UnloadOnly, c.status)

        # Setup Cart
        cart_dev = Cart(4, 150, 0)
        cart_dev.onmove = on_move

        # Setup Cart Controller
        c = CartCtl(cart_dev, Jarvis)

        # Setup Cargo to move
        material = CargoReq('A', 'D', 20, 'material')
        material.onload = on_load
    
        # Setup Plan
        Jarvis.reset_scheduler()
        Jarvis.plan(START_TIME, add_load, (c, material))
        Jarvis.plan(START_TIME + MINUTE, check_cartsnt_status, (c,))
        Jarvis.run()

        # Verify direct output
        log(cart_dev)
        self.assertEqual('unloaded', material.context)

    def test_case_5(self):
        log('== NEW TEST - Test case 5 (8): no request')

        def on_move(c: Cart):
            self.assertEqual(Status.Moving, c.status)
            log('%d: Cart is moving %s->%s' % (Jarvis.time(), c.pos, c.data))

        def check_cart_before(c: Cart):
            self.assertTrue(c.empty())
            self.assertFalse(c.any_prio_cargo())
            self.assertEqual(150, c.load_capacity)
            self.assertEqual(Status.Idle, c.status)

        def check_cart_after(c: Cart):
            self.assertTrue(c.empty())
            self.assertFalse(c.any_prio_cargo())
            self.assertEqual(150, c.load_capacity)
            self.assertEqual(Status.Idle, c.status)

        # Setup Cart
        cart_dev = Cart(4, 150, 0)
        cart_dev.onmove = on_move

        # Setup Cart Controller
        c = CartCtl(cart_dev, Jarvis)

        # Setup Plan
        Jarvis.reset_scheduler()
        Jarvis.plan(5, check_cart_before, (cart_dev,))
        Jarvis.run()

        # Verify direct output
        log(cart_dev)
        check_cart_after(cart_dev)

    def test_combine_1(self):
        log('== NEW TEST - Test combine 1')

        def add_load(c: CartCtl, cargo_req: CargoReq):
            "callback for schedulled load"
            log('%d: Requesting %s at %s' % \
                (Jarvis.time(), cargo_req, cargo_req.src))
            c.request(cargo_req)

        def on_move(c: Cart):
            self.assertEqual(Status.Moving, c.status)
            log('%d: Cart is moving %s->%s' % (Jarvis.time(), c.pos, c.data))

        def on_load(c: Cart, cargo_req: CargoReq):
            "example callback for logging"
            log('%d: Cart at %s: loading: %s' % (Jarvis.time(), c.pos, cargo_req))
            log(c)
            cargo_req.context = "loaded"
            check_cargo_request(cargo_req)
            self.assertIn(cargo_req, c.slots)

        def on_unload(c: Cart, cargo_req: CargoReq):
            "example callback (for assert)"
            log('%d: Cart at %s: unloading: %s' % (Jarvis.time(), c.pos, cargo_req))
            log(c)
            self.assertEqual('loaded', cargo_req.context)
            cargo_req.context = 'unloaded'
            self.assertEqual('B', c.pos)
            self.assertNotIn(cargo_req, c.slots)
            self.assertFalse(cargo_req.prio)

        def check_cargo_request(cargo_req: CargoReq):
            self.assertFalse(cargo_req.prio)
            self.assertEqual('material', cargo_req.content)
            self.assertEqual('A', cargo_req.src)
            self.assertEqual('B', cargo_req.dst)
            self.assertEqual(20, cargo_req.weight)

        # Setup Cart
        cart_dev = Cart(1, 150, 0)
        cart_dev.onmove = on_move

        # Setup Cart Controller
        c = CartCtl(cart_dev, Jarvis)

        # Setup Cargo to move
        material = CargoReq('A', 'B', 20, 'material')
        material.onload = on_load
        material.onunload = on_unload
    
        # Setup Plan
        Jarvis.reset_scheduler()
        Jarvis.plan(START_TIME, add_load, (c, material))
        Jarvis.run()

        # Verify direct output
        log(cart_dev)
        self.assertTrue(cart_dev.empty())
        self.assertEqual('unloaded', material.context)
        self.assertEqual(CStatus.Idle, c.status)

    def test_combine_2(self):
        log('== NEW TEST - Test combine 2')

        def add_load(c: CartCtl, cargo_req: CargoReq):
            "callback for schedulled load"
            log('%d: Requesting %s at %s' % \
                (Jarvis.time(), cargo_req, cargo_req.src))
            c.request(cargo_req)

        def on_move(c: Cart):
            self.assertEqual(Status.Moving, c.status)
            log('%d: Cart is moving %s->%s' % (Jarvis.time(), c.pos, c.data))

        def on_load(c: Cart, cargo_req: CargoReq):
            "example callback for logging"
            log('%d: Cart at %s: loading: %s' % (Jarvis.time(), c.pos, cargo_req))
            log(c)
            cargo_req.context = "loaded"
            if cargo_req.content == 'material':
                self.assertIn(cargo_req, c.slots)
                self.assertEqual('D', c.pos)
            elif cargo_req.content == 'material2':
                self.assertIn(cargo_req, c.slots)
                self.assertEqual('C', c.pos)

        def on_unload(c: Cart, cargo_req: CargoReq):
            "example callback (for assert)"
            log('%d: Cart at %s: unloading: %s' % (Jarvis.time(), c.pos, cargo_req))
            log(c)
            self.assertEqual('loaded', cargo_req.context)
            cargo_req.context = 'unloaded'
            if cargo_req.content == 'material':
                self.assertNotIn(cargo_req, c.slots)
                self.assertEqual('C', c.pos)
            elif cargo_req.content == 'material2':
                self.assertNotIn(cargo_req, c.slots)
                self.assertEqual('B', c.pos)

        # Setup Cart
        cart_dev = Cart(2, 50, 0)
        cart_dev.onmove = on_move

        # Setup Cart Controller
        c = CartCtl(cart_dev, Jarvis)

        # Setup Cargo to move
        material = CargoReq('D', 'C', 30, 'material')
        material.onload = on_load
        material.onunload = on_unload

        material2 = CargoReq('C', 'B', 30, 'material2')
        material2.onload = on_load
        material2.onunload = on_unload
    
        # Setup Plan
        Jarvis.reset_scheduler()
        Jarvis.plan(START_TIME, add_load, (c, material))
        Jarvis.plan(START_TIME + 30, add_load, (c, material2))
        Jarvis.run()

        # Verify direct output
        log(cart_dev)
        self.assertEqual(CStatus.Idle, c.status)
        self.assertTrue(cart_dev.empty())
        self.assertEqual('unloaded', material.context)
        self.assertEqual('unloaded', material2.context)

    def test_combine_3(self):
        log('== NEW TEST - Test combine 3')

        def add_load(c: CartCtl, cargo_req: CargoReq):
            "callback for schedulled load"
            log('%d: Requesting %s at %s' % \
                (Jarvis.time(), cargo_req, cargo_req.src))
            c.request(cargo_req)

        def on_move(c: Cart):
            self.assertEqual(Status.Moving, c.status)
            log('%d: Cart is moving %s->%s' % (Jarvis.time(), c.pos, c.data))

        def on_load(c: Cart, cargo_req: CargoReq):
            "example callback for logging"
            log('%d: Cart at %s: loading: %s' % (Jarvis.time(), c.pos, cargo_req))
            log(c)
            cargo_req.context = "loaded"
            if cargo_req.content == 'material':
                self.assertIn(cargo_req, c.slots)
                self.assertEqual('A', c.pos)
            elif cargo_req.content == 'material2':
                self.assertIn(cargo_req, c.slots)
                self.assertEqual('C', c.pos)

        def on_unload(c: Cart, cargo_req: CargoReq):
            "example callback (for assert)"
            log('%d: Cart at %s: unloading: %s' % (Jarvis.time(), c.pos, cargo_req))
            log(c)
            self.assertEqual('loaded', cargo_req.context)
            cargo_req.context = 'unloaded'
            if cargo_req.content == 'material':
                self.assertNotIn(cargo_req, c.slots)
                self.assertEqual('D', c.pos)
            elif cargo_req.content == 'material2':
                self.assertNotIn(cargo_req, c.slots)
                self.assertEqual('B', c.pos)

        # Setup Cart
        cart_dev = Cart(4, 50, 0)
        cart_dev.onmove = on_move

        # Setup Cart Controller
        c = CartCtl(cart_dev, Jarvis)

        # Setup Cargo to move
        material = CargoReq('A', 'D', 20, 'material')
        material.onload = on_load
        material.onunload = on_unload

        material2 = CargoReq('C', 'B', 20, 'material2')
        material2.onload = on_load
        material2.onunload = on_unload
    
        # Setup Plan
        Jarvis.reset_scheduler()
        Jarvis.plan(START_TIME, add_load, (c, material))
        Jarvis.plan(START_TIME + 10, add_load, (c, material2))
        Jarvis.run()

        # Verify direct output
        log(cart_dev)
        self.assertEqual(CStatus.Idle, c.status)
        self.assertTrue(cart_dev.empty())
        self.assertEqual('unloaded', material.context)
        self.assertEqual('unloaded', material2.context)

    def test_combine_4(self):
        log('== NEW TEST - Test combine 4')

        def add_load(c: CartCtl, cargo_req: CargoReq):
            "callback for schedulled load"
            log('%d: Requesting %s at %s' % \
                (Jarvis.time(), cargo_req, cargo_req.src))
            c.request(cargo_req)

        def on_move(c: Cart):
            self.assertEqual(Status.Moving, c.status)
            log('%d: Cart is moving %s->%s' % (Jarvis.time(), c.pos, c.data))

        def on_load(c: Cart, cargo_req: CargoReq):
            "example callback for logging"
            log('%d: Cart at %s: loading: %s' % (Jarvis.time(), c.pos, cargo_req))
            log(c)
            cargo_req.context = "loaded"
            if cargo_req.content == 'material':
                self.assertIn(cargo_req, c.slots)
                self.assertEqual('A', c.pos)
            elif cargo_req.content == 'material2':
                self.assertIn(cargo_req, c.slots)
                self.assertEqual('A', c.pos)
            elif cargo_req.content == 'material3':
                self.assertIn(cargo_req, c.slots)
                self.assertEqual('C', c.pos)
            elif cargo_req.content == 'material4':
                self.assertIn(cargo_req, c.slots)
                self.assertEqual('B', c.pos)

        def on_unload(c: Cart, cargo_req: CargoReq):
            "example callback (for assert)"
            log('%d: Cart at %s: unloading: %s' % (Jarvis.time(), c.pos, cargo_req))
            log(c)
            self.assertEqual('loaded', cargo_req.context)
            cargo_req.context = 'unloaded'
            if cargo_req.content == 'material':
                self.assertNotIn(cargo_req, c.slots)
                self.assertEqual('B', c.pos)
            elif cargo_req.content == 'material2':
                self.assertNotIn(cargo_req, c.slots)
                self.assertEqual('A', c.pos)
            elif cargo_req.content == 'material3':
                self.assertNotIn(cargo_req, c.slots)
                self.assertEqual('D', c.pos)
            elif cargo_req.content == 'material4':
                self.assertNotIn(cargo_req, c.slots)
                self.assertEqual('A', c.pos)

        # Setup Cart
        cart_dev = Cart(1, 500, 0)
        cart_dev.onmove = on_move

        # Setup Cart Controller
        c = CartCtl(cart_dev, Jarvis)

        # Setup Cargo to move
        material = CargoReq('A', 'B', 150, 'material')
        material.onload = on_load
        material.onunload = on_unload

        material2 = CargoReq('A', 'A', 150, 'material2')
        material2.onload = on_load
        material2.onunload = on_unload

        material3 = CargoReq('C', 'D', 200, 'material3')
        material3.onload = on_load
        material3.onunload = on_unload

        material4 = CargoReq('B', 'A', 200, 'material4')
        material4.onload = on_load
        material4.onunload = on_unload
    
        # Setup Plan
        Jarvis.reset_scheduler()
        Jarvis.plan(START_TIME, add_load, (c, material))
        Jarvis.plan(START_TIME + 10, add_load, (c, material2))
        Jarvis.plan(START_TIME + 20, add_load, (c, material3))
        Jarvis.plan(START_TIME + 30, add_load, (c, material4))
        Jarvis.run()

        # Verify direct output
        log(cart_dev)
        self.assertEqual(CStatus.Idle, c.status)
        self.assertTrue(cart_dev.empty())
        self.assertEqual('unloaded', material.context)
        self.assertEqual('unloaded', material2.context)
        self.assertEqual('unloaded', material3.context)
        self.assertEqual('unloaded', material4.context)

    def test_combine_5(self):
        log('== NEW TEST - Test combine 5')

        def add_load(c: CartCtl, cargo_req: CargoReq):
            "callback for schedulled load"
            log('%d: Requesting %s at %s' % \
                (Jarvis.time(), cargo_req, cargo_req.src))
            c.request(cargo_req)

        def on_move(c: Cart):
            self.assertEqual(Status.Moving, c.status)
            log('%d: Cart is moving %s->%s' % (Jarvis.time(), c.pos, c.data))

        def on_load(c: Cart, cargo_req: CargoReq):
            "example callback for logging"
            log('%d: Cart at %s: loading: %s' % (Jarvis.time(), c.pos, cargo_req))
            log(c)
            cargo_req.context = "loaded"
            if cargo_req.content == 'material':
                self.assertIn(cargo_req, c.slots)
                self.assertEqual('A', c.pos)
            elif cargo_req.content == 'material2':
                self.assertIn(cargo_req, c.slots)
                self.assertEqual('A', c.pos)
            elif cargo_req.content == 'material3':
                self.assertIn(cargo_req, c.slots)
                self.assertEqual('C', c.pos)
            elif cargo_req.content == 'material4':
                self.assertIn(cargo_req, c.slots)
                self.assertEqual('B', c.pos)

        def on_unload(c: Cart, cargo_req: CargoReq):
            "example callback (for assert)"
            log('%d: Cart at %s: unloading: %s' % (Jarvis.time(), c.pos, cargo_req))
            log(c)
            self.assertEqual('loaded', cargo_req.context)
            cargo_req.context = 'unloaded'
            if cargo_req.content == 'material':
                self.assertNotIn(cargo_req, c.slots)
                self.assertEqual('B', c.pos)
            elif cargo_req.content == 'material2':
                self.assertNotIn(cargo_req, c.slots)
                self.assertEqual('A', c.pos)
            elif cargo_req.content == 'material3':
                self.assertNotIn(cargo_req, c.slots)
                self.assertEqual('D', c.pos)
            elif cargo_req.content == 'material4':
                self.assertNotIn(cargo_req, c.slots)
                self.assertEqual('A', c.pos)

        # Setup Cart
        cart_dev = Cart(2, 150, 0)
        cart_dev.onmove = on_move

        # Setup Cart Controller
        c = CartCtl(cart_dev, Jarvis)

        # Setup Cargo to move
        material = CargoReq('A', 'B', 20, 'material')
        material.onload = on_load
        material.onunload = on_unload

        material2 = CargoReq('A', 'A', 20, 'material2')
        material2.onload = on_load
        material2.onunload = on_unload

        material3 = CargoReq('C', 'D', 30, 'material3')
        material3.onload = on_load
        material3.onunload = on_unload

        material4 = CargoReq('B', 'A', 30, 'material4')
        material4.onload = on_load
        material4.onunload = on_unload
    
        # Setup Plan
        Jarvis.reset_scheduler()
        Jarvis.plan(START_TIME, add_load, (c, material))
        Jarvis.plan(START_TIME + 30, add_load, (c, material2))
        Jarvis.plan(START_TIME + 60, add_load, (c, material3))
        Jarvis.plan(START_TIME + 90, add_load, (c, material4))
        Jarvis.run()

        # Verify direct output
        log(cart_dev)
        self.assertEqual(CStatus.Idle, c.status)
        self.assertTrue(cart_dev.empty())
        self.assertEqual('unloaded', material.context)
        self.assertEqual('unloaded', material2.context)
        self.assertEqual('unloaded', material3.context)
        self.assertEqual('unloaded', material4.context)

if __name__ == "__main__":
    unittest.main()
